from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Project(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    total = models.IntegerField()
    positive = models.IntegerField()
    negative = models.IntegerField()
    neutral = models.IntegerField()
    happy = models.IntegerField()
    angry = models.IntegerField()
    image = models.CharField(max_length=100)
    wc = models.BinaryField(blank=True)
    def __str__(self):
        return self.name

