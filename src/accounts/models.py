from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

from .utils import generate_verification_code, send_forgot_password_mail

import logging
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, is_verified=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_verified=is_verified
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_verified=True
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True,)
    email = models.EmailField(verbose_name='Email Address', max_length=60, unique=True)
    is_active = models.BooleanField(default=True) # used by django internally
    is_verified = models.BooleanField(default=False, help_text='Boolean flag states whether the user is verified or not')
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    @property
    def id(self):
        return self.pk

    @property
    def alias(self):
        return self.profile.full_name if hasattr(self, 'profile') else self.username

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Simplest possible answer: Yes, always
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        Simplest possible answer: Yes, always
        """
        return True

    @property
    def is_staff(self):
        """
        Is the user a member of staff?"
        Simplest possible answer: All admins are staff
        """
        return self.is_admin

    def change_password(self, new_password):
        self.passwordutils.change_password(new_password)

    def forgot_password(self):
        self.passwordutils.set_forgot_password()

    def verify(self, verification_code):
        if not self.is_verified:
            return self.verification.verify_user(verification_code)
        raise ValidationError('User already Verified')

    def refresh_verification(self):
        if not self.is_verified:
            return self.verification.refresh()
        raise ValidationError('User already Verified')


class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    def verify_user(self, code):
        if code == self.code:
            self.user.is_verified = True
            self.user.save()
            logger.info(f'Activating the user {self.user.username}')
            self.delete()
        else:
            raise ValidationError('Incorrect Activation Code')

    def refresh(self):
        self.code = generate_verification_code()
        logger.info(f'Refreshed Verification Token for {self.user.username}')
        self.save()

    def __str__(self):
        return self.user.username


class PasswordUtils(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forgot_password = models.BooleanField(default=False)
    forgot_password_code = models.CharField(max_length=12)

    class Meta:
        verbose_name = 'Password Utils'
        verbose_name_plural = 'Password Utils'

    def set_forgot_password(self):
        self.forgot_password = True
        self.forgot_password_code = generate_verification_code(12)
        self.save()
        send_forgot_password_mail(self.user.username, self.forgot_password_code, self.user.email)

    def change_password_anonymous(self, new_password):
        if not self.forgot_password:
            raise ValidationError('BAD REQUEST')

        self.forgot_password = False
        self.forgot_password_code = ''
        self.change_password(new_password)
        self.save()

    def change_password(self, new_password):
        if self.user.check_password(new_password):
            raise ValidationError('New Password cannot be the same as old password')
        self.user.set_password(new_password)
        self.user.save()

    def __str__(self):
        return self.user.username
