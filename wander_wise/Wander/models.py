#from django.db import models
# Create your models here.

from django.db import models
from django.contrib.auth.models import User  # Import the User model



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

def __str__(self):
        return self.user.username

class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide', null=True)  # Allow null temporarily
    languages_known = models.CharField(max_length=100)
    places_known = models.CharField(max_length=100)
    govt_id = models.CharField(max_length=100)
    quiz_score = models.IntegerField(default=0)  # Default value for quiz score

    def __str__(self):
        return self.user.username  # Return the email of the associated user or "No User" if user is