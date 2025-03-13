from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/',views.SignupView.as_view(),name='user-sign_up'),
    path('otp_verification/',views.OptVerificationView.as_view(),name='otp-verification'),
    path('',views.user_login,name='user-login'),
    path('user-home/',views.user_home,name='user-home'),
    path("user_logout/", views.UserLogoutView.as_view(), name="user-logout"),
]
