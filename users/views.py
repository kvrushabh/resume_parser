from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone

# imports for database models
from .models import Profile
from django.contrib import messages

# imports for authentications
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# imports for automated mails
import uuid
import random
from django.conf import settings
from django.core.mail import send_mail


def handlesignup(request):
    if request.method == 'POST':
        # Get the all parameters
        user_name = request.POST.get('user_name')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('Confirm Password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')


        # checks for error inputs
        if (password != confirm_password):
            messages.error(request, "Passwords do not match")
            return redirect('upload_resume')
    
        if User.objects.filter(username = user_name).exists():
                messages.warning(request,'Username is already Taken! Try unique username...')
                return redirect('upload_resume')

        if User.objects.filter(email = email_id).exists():
                messages.warning(request,'Email id is already Exist, Try different Email !')
                return redirect('upload_resume')

        # create the user
        myuser = User.objects.create_user(user_name, email_id, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        otp = random.randint(100000, 999999)

        auth_token = str(uuid.uuid4())
        forgot_password_token = str(uuid.uuid4())

        profile_obj = Profile.objects.create(user = myuser, auth_token = auth_token, forgot_password_token=forgot_password_token, otp=otp)
        profile_obj.save()

        # verification not working currently
        # send_mail_after_registration(email_id, auth_token)
        
        messages.success(request, f"Hi {user_name}, kindly verify your account through the mail")
    return redirect("upload_resume")


def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')
        
        user_obj = User.objects.filter(username = loginusername).first()
        if user_obj is None:
            messages.error(request, f"Enter a valid username")
            return redirect("upload_resume")

        profile_obj = Profile.objects.filter(user = user_obj ).first()
        if not profile_obj.is_verified:
            messages.warning(request, 'Your account is not verified, check your mails.')
            return redirect('upload_resume')

        user = authenticate(username= loginusername, password= loginpassword)
        if user is None:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("upload_resume")

        login(request, user)
        messages.success(request, f"Successfully Logged In as {loginusername}")
        return redirect("upload_resume")
    else:
        return HttpResponse("404- Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('upload_resume')





# for email id verification

# link method
def email_verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, f'Your account is already verified.')
                return redirect('upload_resume')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, f"Your account has been verified, Now you can login")
            return redirect('upload_resume')
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('upload_resume')
    except Exception as e:
        print(e)
        return redirect('upload_resume')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, Click the link to verify your email address http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from, recipient_list)



# for forgot passsword
def changepassword(request, token):
    params = {}
    
    try:
        Profile_obj = Profile.objects.filter(forgot_password_token = token).first()
        params= {'user_id': Profile_obj.user_id}

        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('cpassword')
            user_id = request.POST.get('user_id')       
                
            if new_password != confirm_password:
                messages.error(request, "both password should be equal.")
                return redirect(f'/change-password/{token}')

            print( Profile_obj.id,user_id, Profile_obj.user_id)
                
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()

            messages.success(request, "Your password is updated.")
            return redirect('upload_resume')

    except Exception as e:
        print(e)

    return render(request, 'resumes/change-password.html', params)


def forgetpassword(request):
    if request.method == "POST":
        username = request.POST.get('username')

        if not User.objects.filter(username = username).first():
            messages.error(request, 'No user found with this username')
            return redirect('upload_resume')

        user_obj = User.objects.get(username = username)
        token = str(uuid.uuid4())

        Profile_obj = Profile.objects.get(user = user_obj)
        Profile_obj.forgot_password_token = token
        Profile_obj.save()

        send_forgot_password_email(user_obj.email, token)

        messages.success(request, 'An email has been send to register email id')
        return redirect('upload_resume')

    return render(request,"resumes/forgot-password.html")


def send_forgot_password_email(email, token):
    subject = 'Forgot password link'
    message = f'Hi, click the link to change the password http://127.0.0.1:8000/change-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)