from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from .utils import calculate_quiz_score  # Import the function to calculate quiz score
from .models import Profile,Guide,VisitPlan,RateBit,Feedback
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login ,logout as django_logout # Renaming the login function
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseBadRequest
from django.core.mail import send_mail


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
            print("Authentication successful.")  # Debug print statement

            try:
                profile = Profile.objects.get(user_id=user.id)  # Retrieve the profile associated with the user ID
                print("Profile found:", profile)  # Debug print statement

                # Now you have both user and profile, you can use them as needed
                # For example, you can access user.email, user.first_name, etc.
                # Similarly, you can access profile attributes like profile.phone, profile.gender, etc.
                
                if profile.user_type.lower() == 'visiter':
                    # messages.success(request, 'Logged in as visitor!')
                    auth_login(request, user)  # Log in the user

                    return redirect('visitor')  # Redirect to visitor dashboard
                elif profile.user_type.lower() == 'guide':
                    if hasattr(profile, 'guide'):  # Check if Guide profile exists
                        guide = profile.guide  # Retrieve the associated guide profile
                        if guide.quiz_score >= 6:  # If the user is a guide and already scored 6 or more
                            # messages.success(request, 'Logged in as guide!')
                            auth_login(request, user)  # Log in the user
                            return redirect('guideinterface')
                        else:
                            messages.success(request, 'Please complete the exam!')
                            auth_login(request, user)  # Log in the user

                            return redirect('exam')
                    else:
                        #messages.success(request, 'Please complete the exam!')
                        auth_login(request, user)  # Log in the user

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

@login_required
def visitor(request):
    user = request.user
    if user.is_authenticated:
        # Fetch visit plans generated by the visitor
        visit_plans = VisitPlan.objects.filter(user=user)
        #Fetch booked
        booked_guides = RateBit.objects.filter(visit_plan__isBooked=True)
        # Fetch rate responses for the visit plans
        rate_responses = RateBit.objects.filter(visit_plan__in=visit_plans).order_by('-insert_datetime')
        #guide contact
        profile = Profile.objects.get(user=user)

        context = {
            'user': user,
            'profile':profile,
            'booked_guides':booked_guides,
            'rate_responses': rate_responses
        }
        return render(request, 'visitor.html', context)
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('login')
def logout(request):
    django_logout(request)  # Use Django's logout function to logout the user
    return redirect('index')
@login_required
def exam(request):
    if request.method == 'POST':
        print("exam submitted successfully!") 
        languages_known = request.POST.get('languages_known')
        places_known = request.POST.get('places_known')
        govtIdType = request.POST.get('govtIdType')
        govt_id = request.POST.get('govt_id')
        quiz_score = calculate_quiz_score(request.POST)  # You need to implement this function

        # Create a new Guide instance associated with the logged-in user and save it to the database
        guide_instance = Guide.objects.create(
            user=request.user,  # Associate the guide with the logged-in user
            languages_known=languages_known,
            places_known=places_known,
            govtIdType=govtIdType,
            govt_id=govt_id,
            quiz_score=quiz_score
        )
        guide.save()  # Call .save() to persist data to the database
        return redirect('guideinterface') # Redirect to a success page

    try:
        guide = Guide.objects.get(user=request.user)
        if guide and guide.quiz_score >= 6:
            # If the user has already completed the exam and scored 6 or more, redirect to the guide interface
            return redirect('guideinterface')
    except Guide.DoesNotExist:
        pass  # User hasn't completed the exam yet, continue to render the exam page

    # If the user hasn't completed the exam or hasn't scored 6 or more, render the exam page
    return render(request, 'exam.html')

# class exam(View):
#     def get(self,request):
#         form = ExamForm()
#         return render(request,'templates/exam.html',{'form':form})
    
#     def post(self,request):
#         form = ExamForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return render(request,'templates/exam.html',{'form':form})

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
                #Fetch booked
                booked_visits = VisitPlan.objects.filter(isBooked=True, ratebit__guide=user).distinct()
                
                context = {
                    'qualified_users': qualified_users,
                    'avg_quiz_score': avg_quiz_score,
                    'booked_visits':booked_visits,
                    'guide':guide,
                }
                visit_plans = VisitPlan.objects.filter(isBooked=False).order_by('-insertDateTime')
                return render(request, 'guideinterface.html', {'visit_plans': visit_plans,**context})
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

def Visitplan(request):
    if request.method == 'POST':
        print("Form submitted successfully!")  # Debugging statement

        city = request.POST.get('city')
        place = request.POST.get('place')
        from_date_time = request.POST.get('from_date_time')
        to_date_time = request.POST.get('to_date_time')

        print("City:", city)  # Debugging statement
        print("Place:", place)  # Debugging statement
        print("From Date & Time:", from_date_time)  # Debugging statement
        print("To Date & Time:", to_date_time)  # Debugging statement

        # Validate form data
        if not city or not place or not from_date_time or not to_date_time:
            return HttpResponse("All fields are required.", status=400)  # Bad request

        try:
            # Create a VisitPlan object
            visit_plan_instance = VisitPlan.objects.create(
                user=request.user,
                city=city,
                place=place,
                from_date_time=from_date_time,
                to_date_time=to_date_time
            )
            try:
    # Get all guide users from the database
                 guides = Guide.objects.all()

            # Get the email address of the guide
                 recipient_list = [guide.user.username for guide in guides]

            # Compose the email message
                 subject = 'New Visit Request'
                 message = 'A new visit request has been generated. Please check your dashboard.'
                 from_email = 'shuklamentos@gmail.com'

            # Send email notifications to guides
                 try:
                     send_mail(subject, message, from_email, recipient_list)
                     print("Email sent successfully.")  # Debugging statement
                 except Exception as e:
                     print("Error sending email:", str(e))  # Debugging statement

            except Exception as e:
                    print("Error:", str(e))  # Debugging statement

            # Return success message

            return redirect('visitor')
        except Exception as e:
            # Handle database integrity error
            return HttpResponse(f"An error occurred: {str(e)}", status=500)  # Internal Server Error

    else:
        # If the request method is not POST, handle it accordingly (e.g., render a form)
        return render(request, 'visitor.html')

def submitamount(request):
    if request.method == 'POST':
        # Check CSRF token
        if not request.POST.get('csrfmiddlewaretoken'):
            return HttpResponseBadRequest("CSRF token missing or invalid.")

        # Get data from POST request
        visit_plan_id = request.POST.get('visit_plan_id')
        guide_id = request.POST.get('guide_id')
        rate_amount = request.POST.get('rate_amount')

        # Validate form data
        if not (visit_plan_id and guide_id and rate_amount):
            return HttpResponseBadRequest("Missing required data.")

        # Get the visit plan and guide objects
        try:
            visit_plan = VisitPlan.objects.get(id=visit_plan_id)
            guide = User.objects.get(id=guide_id)
        except VisitPlan.DoesNotExist:
            return HttpResponseBadRequest("Invalid visit plan ID.")
        except User.DoesNotExist:
            return HttpResponseBadRequest("Invalid guide ID.")

        # Create and save the RateBit instance
        try:
            rate_bit = RateBit.objects.create(
                visit_plan=visit_plan,
                guide=guide,
                rate_amount=rate_amount
            )
            try:
              # Get the visitor user who submitted the visit request
                 visitor = visit_plan.user
            # Get the email address of the guide
                 recipient_list = [visitor.username]

            # Compose the email message
                 subject = 'Payment Response from Guide'
                 message = f'Hi {visitor.first_name},\n\nYou have a payment response from {guide.first_name} {guide.last_name} for your visit request with details:\n\nVisit Plan ID: {visit_plan_id}\nVisit Place:{visit_plan.place}\nRate Amount: {rate_amount}\n\nPlease check the website for more details.\n\nBest regards,\nWanderwise Team'
                 from_email = 'shuklamentos@gmail.com'

            # Send email notifications to guides
                 try:
                     send_mail(subject, message, from_email, recipient_list)
                     print("Email sent successfully.")  # Debugging statement
                 except Exception as e:
                     print("Error sending email:", str(e))  # Debugging statement

            except Exception as e:
                    print("Error:", str(e))  # Debugging statement
            return redirect('guideinterface')
        except Exception as e:
            return HttpResponseBadRequest(f"Failed to submit rate amount: {e}")

    else:
        return HttpResponseBadRequest("Only POST requests are allowed for this endpoint.")


def book_guide(request):
    if request.method == 'POST':
        visit_plan_id = request.POST.get('visit_plan_id')
        try:
            visit_plan = VisitPlan.objects.get(pk=visit_plan_id)
            if not visit_plan.isBooked:
                visit_plan.isBooked = True
                visit_plan.save()
                return redirect('visitor')
            else:
                return HttpResponse("Guide is already booked!", status=400)
        except VisitPlan.DoesNotExist:
            return HttpResponse("Visit plan does not exist!", status=400)
    else:
        return HttpResponse("Invalid request!", status=400)
    
def payment(request):
    if request.method == 'POST':
        mode_of_payment = request.POST.get('modeOfPayment')
        is_completed = request.POST.get('isCompleted') == 'true'

        # Assuming you have a way to identify the visit plan, for example, its ID
        visit_plan_id = request.POST.get('visitPlanId')  # Add a hidden input field in your form to store visit plan ID

        try:
            visit_plan = VisitPlan.objects.get(id=visit_plan_id)
            # Update the visit plan fields
            visit_plan.modeOfPayment = mode_of_payment
            visit_plan.isCompleted = is_completed
            visit_plan.save()
            
            # Optionally, you can add a message to be displayed after successful submission
            return redirect('visitor')
        except VisitPlan.DoesNotExist:
            return HttpResponse("Visit plan does not exist!")
    
    return HttpResponse("Invalid request method.")

def payment_confirm(request):
    if request.method == 'POST':
        visit_plan_id = request.POST.get('pay_confirm')
        try:
            visit_plan = VisitPlan.objects.get(pk=visit_plan_id)
            if not visit_plan.isPaid:
                visit_plan.isPaid = True
                visit_plan.save()
                try:
              # Get the visitor user who submitted the visit request
                 visitor = visit_plan.user
            # Get the email address of the guide
                 recipient_list = [visitor.username]

            # Compose the email message
                 subject = 'Come Visit Us Again!'
                 message = """
We hope this message finds you well.

Thank you for choosing WanderWise for your recent trip. We trust that your experience was enjoyable and memorable.

Your feedback matters greatly to us! We invite you to share your thoughts about your trip by providing feedback on our website. Your valuable insights will help us improve our services and ensure that future visits are even more fulfilling.

As a token of appreciation for your time, we would like to extend a special invitation for you to visit us again. Whether it's exploring new destinations or revisiting your favorite spots, we're here to make every journey exceptional for you.

We look forward to welcoming you back soon!
"""

                 from_email = 'shuklamentos@gmail.com'

            # Send email notifications to guides
                 try:
                    send_mail(subject, message, from_email, recipient_list)
                    print("Email sent successfully.")  # Debugging statement
                 except Exception as e:
                    print("Error sending email:", str(e))  # Debugging statement

                except Exception as e:
                    print("Error:", str(e))  # Debugging statement
                return redirect('guideinterface')
            else:
                return HttpResponse("not paid!", status=400)
        except VisitPlan.DoesNotExist:
            return HttpResponse("Visit plan does not exist!", status=400)
    else:
        return HttpResponse("Invalid request!",status=400)
    

def submit_feedback(request):
    user = request.user
    if request.method == 'POST':
        if request.user.is_authenticated:
            feedback_text = request.POST.get('feedback', '')
            rating = request.POST.get('rating', '')

            # Create a new Feedback object and save it to the database
            feedback = Feedback.objects.create(
                user=request.user,
                feedback=feedback_text,
                rating=rating
            )

            # Redirect to a thank you page or any other page you want to display after submission
            if user.is_authenticated and user.profile.user_type == 'Guide':
                 return redirect('guideinterface')
            else:
                 return redirect('visitor')
        else:
            # Handle the case when the user is not authenticated
            return HttpResponse('no user') # Redirect to the login page

    # If the request method is not POST, render the feedback form template
    return render(request, 'feedback_form.html')  # Replace 'feedback_form.html' with the actual template name