from ..models import Profile
from .serlizer import ProfileSerlizer
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from core.premission import IsOwner
from .serlizer import ProfileSerlizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView

@api_view(["GET"])  
@permission_classes([IsAuthenticated])
def get_profile(request):
    
    profile= Profile.objects.get(user=request.user)
    ser= ProfileSerlizer(profile)
    return Response(ser.data,status=status.HTTP_200_OK) 
    
  
   
#! updae profile
class UpdateProfile(UpdateAPIView):
    queryset= Profile.objects.all()
    serializer_class= ProfileSerlizer
    permission_classes= [IsAuthenticated, IsOwner]
    def get_object(self):
        return self.request.user.profile
   
    @method_decorator(ratelimit(key="ip",rate="3/h",block=True,method="PATCH"))   
    def perform_update(self, Serializer):
        profile= self.get_object()
        if profile.user!= self.request.user:
            return Response("you can only edit own profile")
        Serializer.save()
        return Response({
            "message": "Profile updated successfully."
        }, status=status.HTTP_200_OK)
     