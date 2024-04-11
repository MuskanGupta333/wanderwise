#from django.db import models
# Create your models here.

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Making email field unique
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    password = models.CharField(max_length=100)


def __str__(self):
        return self.email