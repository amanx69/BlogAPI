from django.urls import path
from .views import get_my_profile ,UpdateProfile, get_target_profile

urlpatterns = [
    path("Profile/",get_my_profile,name="get_my_profile"),
    path("Profile/update/",UpdateProfile.as_view(),name="update_profile"),
    path("targetProfile/<int:user_id>/",get_target_profile,name="get_target_profile")
]


