from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    image_url = models.URLField(blank=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' if self.last_name else self.first_name