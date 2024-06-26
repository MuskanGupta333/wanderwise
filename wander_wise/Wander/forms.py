from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Guide  # Import the Guide model
from .models import VisitPlan


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class Guide(forms.ModelForm):

    class Meta:
        model = Guide  # Use the Guide model since the exam is for becoming a guide
        fields = ['languages_known', 'places_known','govtIdType', 'govt_id']

    # def clean_languages_known(self):
    #     languages_known = self.cleaned_data['languages_known']
    #     # Validate languages known here if needed
    #     return languages_known

    # def clean_places_known(self):
    #     places_known = self.cleaned_data['places_known']
    #     # Validate places known here if needed
    #     return places_known
    
    # def clean_govtIdType(self):
    #     places_known = self.cleaned_data['govtIdType']
    #     # Validate places known here if needed
    #     return govtIdType # type: ignore
    
    # def clean_govt_id(self):
    #     govt_id = self.cleaned_data['govt_id']
    #     # Validate government ID here if needed
    #     return govt_id
    class VisitPlan(forms.ModelForm):
        class Meta:
           model = VisitPlan
           fields = ['city', 'place', 'from_date_time', 'to_date_time']
           widgets = {
            'from_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'to_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

   