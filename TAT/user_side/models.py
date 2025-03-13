from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.utils.timezone import now, timedelta
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='user-profile-pics/',blank=True,null=True)
    is_email_verified = models.BooleanField(default=False)


def default_expiry():
    return now() + timedelta(minutes=2)

class OTPVerification(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, related_name='otp_verification')
    otp = models.CharField(max_length=4,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default= default_expiry)

    def is_expired(self):
        return now() > self.expires_at

    def otp_generate(self):
        self.otp = str(random.randint(1000,9999))
        self.created_at = now()
        self.expires_at = now() + timedelta(minutes=2)
        self.save()

    


