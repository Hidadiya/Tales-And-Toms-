from django.core.mail import send_mail
from django.utils.timezone import now
from .models import OTPVerification


def send_otp_email(user):
    otp_entry, created = OTPVerification.objects.get_or_create(user=user)

    if not created and not otp_entry.is_expired():
        return False
    
    otp_entry.otp_generate()

    """ Welcome To Our website"""
    subject = 'Welcome To Our website.This email will give you the OTP to verify your email'
    message = f'Dear User {user.username}, \n\n Your OTP is: {otp_entry.otp}\n\nPlease enter this OTP to verify your account.'
    from_email = 'Yazra3119@gmail.com'
    reciver_email = [user.email]

    send_mail(subject,message,from_email,reciver_email)
    return True

