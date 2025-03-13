from django.shortcuts import render,redirect
from django.contrib.auth import login , authenticate
from django.views import View
from .models import CustomUser,OTPVerification
from .forms import UserSignupForm,OtpForm
from .utils import send_otp_email
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


#This is for user_ signing up and sending the otp
class SignupView(View):
    def get(self,request):
        form = UserSignupForm()
        return render(request,'user/user-signup.html',{'form':form})



    def post(self,request):
        form =UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_otp_email(user)
            request.session['pending_user']=user.email
            return redirect('otp-verification')
        return render(request,'user/user-signup.html',{'form':form})
    



class OptVerificationView(View):
    def get(self,request):
        form = OtpForm()
        return render(request,'user/user-otp.html',{'form':form})
    


    def post(self,request):
        form = OtpForm(request.POST)
        email = request.session.get('pending_user')
        user = CustomUser.objects.filter(email=email).first()

        if user and form.is_valid():
            otp_verification = OTPVerification.objects.filter(user=user).first()
            otp_code = otp_verification.otp
            entered_code = form.cleaned_data['otp']
            if entered_code == otp_code:
                if otp_verification.is_expired():
                    form.add_error('otp', 'OTP has expired')
                else:
                    user.is_active=True
                    user.is_email_verified=True
                    otp_verification.otp = None
                    otp_verification.save()
                    user.save()
                    login(request,user)
                    return redirect('user-home')
            else:
                form.add_error('otp','Invalid otp')
        return render(request,'user/user-otp.html',{'form':form})
    


def user_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'user/user-login.html', {'form': form})
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print('request.POST')
        if form.is_valid():
            print('form')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"username :{username} and password:{password}")
            user = authenticate(username=username,password=password)

            if user is not None:
                custom_user = CustomUser.objects.get(username=username)
                print(custom_user.is_email_verified)
                print(custom_user.is_active)
            
                if custom_user.is_email_verified:
                    print(custom_user.is_email_verified)
                    print(custom_user.is_active)
                    login(request, custom_user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('user-home')
                else:
                    send_otp_email(custom_user)
                    print(custom_user.is_email_verified)
                    print(custom_user.is_active)
                    request.session['pending_user']=custom_user.email
                    print(custom_user.is_email_verified)
                    print(custom_user.is_active)
                    print(request.session)
                    return redirect('otp-verification')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            print('from is not valid')
            messages.error(request, "Invalid login details.")

    return render(request,'user/user-login.html',{'form':form})
#
    
def user_home(request):
    return render(request,'user/user-home.html')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("user-login")
        
    



    



