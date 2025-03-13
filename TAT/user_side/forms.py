from django import forms
from user_side.models import CustomUser
from django.contrib.auth.forms import UserCreationForm



class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']



class OtpForm(forms.Form):
    otp = forms.CharField(
        max_length=4,
        min_length=4,
        required=True,
        error_messages={
            "required": "OTP is required", "min_length": "OTP must be 4 digits", "max_length": "OTP must be 4 digits"}
            )