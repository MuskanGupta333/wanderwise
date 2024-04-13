from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password #make_password

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Check if user exists in the signup table
            user = User.objects.get(email=email)
            # Verify the password
            if check_password(password, user.password):
                if user.user_type == 'Visiter':
                    messages.success(request, 'Logged in as visitor!')
                    return redirect('visitor')  # Redirect to visitor dashboard
                elif user.user_type == 'Guide':
                    messages.success(request, 'Logged in as guide!')
                    return redirect('guideinterface')  # Redirect to guide dashboard
                else:
                    messages.error(request, 'Invalid user type.')
            else:
                # Password doesn't match
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            # User does not exist in the User table
            messages.error(request, 'User does not exist. Please sign up first.')
    return render(request, 'login.html')  # Render login page template

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        user_type = request.POST.get('user_type')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address = request.POST.get('address')
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
        else:
        
            # Hash the password
            hashed_password = make_password(password)
            # Create a new user instance
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,  # Use hashed password                phone=phone,
                gender=gender,
                user_type=user_type,
                pincode=pincode,
                city=city,
                state=state,
                country=country,
                address=address
            )
            # Save the user object to the database
            user.save()
            # Display a success message
            messages.success(request, 'Signed up successfully! Please log in.')
            # Redirect to the login page
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

def visitor(request):
    return render(request, 'visitor.html')
def guideinterface(request):
    return render(request, 'guideinterface.html')
