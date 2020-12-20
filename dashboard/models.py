from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    user=models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    file=models.CharField(max_length=100)

    def __str__(self):
        return self.name