from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email, password=password)
            messages.success(request, 'Logged in successfully!')
            # You can redirect the user to a dashboard or profile page after login
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.save()
            messages.success(request, 'Signed up successfully! Please log in.')
            return redirect('login')
    return render(request, 'signup.html')

def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')
def service(request):
    return render(request, 'service.html')
def appointment(request):
    return render(request, 'appointment.html')
def be_a_guide(request):
    return render(request, 'be_a_guide.html')
def feature(request):
    return render(request, 'feature.html')
def testimonial(request):
    return render(request, 'testimonial.html')
