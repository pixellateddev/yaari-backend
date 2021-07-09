from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

from .utils import generate_verification_code

import logging
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
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
        )
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.EmailField(verbose_name='Email Address', max_length=60, unique=True)
    is_active = models.BooleanField(default=True) # used by django internally
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = UserManager()

    @property
    def id(self):
        return self.pk

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
