#from django.db import models
# Create your models here.

from django.db import models
from django.contrib.auth.models import User  # Import the User model
from django.utils import timezone




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
  
    
    ID_CHOICE=[
     ('PAN','PAN Card'),
     ('Aadhar','Aadhar Card'),   
     ]


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide', null=True)  # Allow null temporarily
    languages_known = models.CharField(max_length=100) #,choices=LANGUAGE_CHOICES)
    places_known = models.CharField(max_length=100) #,choices=PLACES_CHOICES)
    govtIdType = models.CharField(max_length=30,choices=ID_CHOICE)
    govt_id = models.CharField(max_length=100,default='')
    quiz_score = models.IntegerField(default=0)  # Default value for quiz score
    

    def __str__(self):
        return self.user.username  # Return the email of the associated user or "No User" if user is
    

class VisitPlan(models.Model):
    CITY_CHOICES = [
        ('1', 'Lucknow'),
    ]

    PLACE_CHOICES = [
        ('1', 'Lucknow Zoo'),
        ('2', 'Bara Imambara'),
        ('3', 'Chota Imambara'),
        ('4', 'Rumi Darwaza'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    place = models.CharField(max_length=100, choices=PLACE_CHOICES)
    from_date_time = models.DateTimeField()
    to_date_time = models.DateTimeField()
    isActive = models.BooleanField(default=True)  # New field for active status
    isBooked = models.BooleanField(default=False)  # New field for booking status
    insertDateTime = models.DateTimeField(default=timezone.now)  # New field for insertion datetime

    def __str__(self):
        return f"Visit Plan for {self.get_place_display()} in {self.get_city_display()}" 
    
    ''' LANGUAGE_CHOICES =[
         ('Hindi','Hindi'),
         ('English','English'),
         ('Urdu','Urdu'),
         ('Arabi','Arabi'),
         ('Korean','Korean'),
         ('Japanese','Japanese'),
         ('French','French'),
         ('Spanish','Spanish'),
    ]
    PLACES_CHOICES=[
         ('1','Bara Imambara'),
         ('2','Chota Imambara'),
         ('3','Rumi Darwaza'),
         ('4','Lucknow Zoo'),
         ('5','Residency'),'''
