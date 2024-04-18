from django.shortcuts import render, redirect
from django.contrib import messages
#from .models import User,Guide
#from django.contrib.auth.hashers import make_password, check_password #make_password
from django.db.models import Avg
from .utils import calculate_quiz_score  # Import the function to calculate quiz score
from .models import Profile,Guide
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login  # Renaming the login function
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()  # Trim whitespace
        password = request.POST.get('password')
        print("Email entered:", email)  # Debug print statement
        print("Password entered:", password)  # Debug print statement

        # Authenticate user using email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:  # User authentication successful
            try:
                profile = Profile.objects.get(user=user)  # Retrieve the profile associated with the user
                print("Profile found:", profile)  # Debug print statement

                if profile.user_type == 'Visiter':
                    messages.success(request, 'Logged in as visitor!')
                    return redirect('visitor')  # Redirect to visitor dashboard
                elif profile.user_type == 'Guide':
                    if hasattr(profile, 'guide'):  # Check if Guide profile exists
                        guide = profile.guide  # Retrieve the associated guide profile
                        if guide.quiz_score >= 6:  # If the user is a guide and already scored 6 or more
                            messages.success(request, 'Logged in as guide!')
                            auth_login(request, user)  # Log in the user
                            return redirect('guideinterface')
                        else:
                            messages.success(request, 'Please complete the exam!')
                            return redirect('exam')
                    else:
                        messages.success(request, 'Please complete the exam!')
                        return redirect('exam')
                else:
                    messages.error(request, 'Invalid user type.')
            except Profile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            print("Authentication failed.")  # Debug print statement
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        # Get form data
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
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create profile
            profile = Profile.objects.create(
                user=user,
                phone=phone,
                gender=gender,
                user_type=user_type,
                pincode=pincode,
                city=city,
                state=state,
                country=country,
                address=address
            )

            # Display success message
            messages.success(request, 'Signed up successfully! Please log in.')
            # Redirect to login page
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
@login_required

def exam(request):
    if request.method == 'POST':
        languages_known = request.POST.get('languagesKnown')
        places_known = request.POST.get('placesKnown')
        govt_id = request.POST.get('govtId')
        quiz_score = calculate_quiz_score(request.POST)  # You need to implement this function

        # Create a new Guide instance associated with the logged-in user and save it to the database
        guide = Guide.objects.create(
            user=request.user,  # Associate the guide with the logged-in user
            languages_known=languages_known,
            places_known=places_known,
            govt_id=govt_id,
            quiz_score=quiz_score
        )
        guide.save()  # Call .save() to persist data to the database
        return redirect('guideinterface')  # Redirect to a success page

    try:
        guide = Guide.objects.get(user=request.user)
        if guide and guide.quiz_score >= 6:
            # If the user has already completed the exam and scored 6 or more, redirect to the guide interface
            return redirect('guideinterface')
    except Guide.DoesNotExist:
        pass  # User hasn't completed the exam yet, continue to render the exam page

    # If the user hasn't completed the exam or hasn't scored 6 or more, render the exam page
    return render(request, 'exam.html')

@login_required
def guideinterface(request):
    user = request.user
    if user.is_authenticated and user.profile.user_type == 'Guide':
        try:
            guide = Guide.objects.get(user=user)  # Retrieve the associated guide profile
            if guide and guide.quiz_score >= 6:
                # Fetch qualified guides and calculate average quiz score
                qualified_guides = Guide.objects.filter(quiz_score__gte=6)
                avg_quiz_score = qualified_guides.aggregate(Avg('quiz_score'))['quiz_score__avg']
                # Retrieve emails of qualified users
                qualified_emails = [g.user.email for g in qualified_guides if g.user and g.user.email]
                # Fetch qualified users with emails
                qualified_users = User.objects.filter(email__in=qualified_emails)
                context = {
                    'qualified_users': qualified_users,
                    'avg_quiz_score': avg_quiz_score,
                }
                return render(request, 'guideinterface.html', context)
            else:
                # Redirect to the exam page if the user's quiz score is less than 6
                messages.error(request, 'Please complete the exam!')
                return redirect('exam')
        except Guide.DoesNotExist:
            # Handle the case where the user doesn't have a guide profile
            messages.error(request, 'Please complete the exam!')
            return redirect('exam')
    else:
        # Redirect to login page if the user is not authenticated or not a guide
        messages.error(request, 'Access denied!')
        return redirect('login')

