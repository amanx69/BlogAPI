from django.urls import path
from .views import Signup,Loginview, VerifyEmail, ResendVerificationView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
     path("signup/",Signup.as_view(),name="signup"),
     path("login/",Loginview.as_view(),name= "login"),
     path("verify-email/<uid>/<token>/",VerifyEmail.as_view(),name="verify_email"),
     path("resent-ver/",ResendVerificationView.as_view(),name= "resendcode"),
     path("token/refresh/",TokenRefreshView.as_view(),name="refresh_token"),
     path("Logout/",LogoutView.as_view(),name= "logout")
    
]


