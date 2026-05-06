from django.urls import path
from .views import get_profile ,UpdateProfile

urlpatterns = [
    path("Profile/",get_profile,name="get_profile"),
    path("Profile/update/",UpdateProfile.as_view(),name="update_profile")
]