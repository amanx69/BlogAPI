from ..models import Profile
from .serlizer import ProfileSerlizer
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
from core.premission import IsOwner
from .serlizer import UpdateProfileSerlizer ,ProfileSerlizer ,TragetProfileSerlizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import get_user_model
from apps.post.models import Post
from apps.post.api.seriilizers import Postserlizers
User = get_user_model()

@api_view(["GET"])  
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    cache_key = f"my_profile_{request.user.id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response(cached_data, status=status.HTTP_200_OK)

    try:
        user_posts = Post.objects.filter(user=request.user)
        posts_data = Postserlizers.PostDetailSerializer(user_posts, many=True).data

        profile = User.objects.select_related('profile').get(id=request.user.id).profile
        profile_data = ProfileSerlizer(profile).data

    except User.profile.RelatedObjectDoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    response_data = {
        "profile": profile_data,
        "posts": posts_data,
        "post_count": user_posts.count()
    }

    cache.set(cache_key, response_data, timeout=5 * 60)  #! Cache for 5 minutes

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_target_profile(request,user_id):
    cache_key = f"target_profile_{user_id}"
    profile_data = cache.get(cache_key)
    if  profile_data:
        return Response(profile_data, status=status.HTTP_200_OK)
    try:
        user_post= Post.objects.filter(user_id=user_id)
        posts_data = Postserlizers.PostDetailSerializer(user_post, many=True).data
        profile = User.objects.select_related('profile').get(id=user_id).profile
        user_profile = TragetProfileSerlizer(profile).data
    except User.profile.RelatedObjectDoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
    except Exception  as e :
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    response={
        "profile": user_profile,
        "user_post": posts_data,
        "post_count": user_post.count()
    }
    cache.set(cache_key, response, timeout=5 * 60)  
    return Response(response, status=status.HTTP_200_OK)

    
    
    
    
  
   
#! updae profile


class UpdateProfile(UpdateAPIView):
    queryset= Profile.objects.all()
    serializer_class= UpdateProfileSerlizer
    permission_classes= [IsAuthenticated, IsOwner]
    def get_object(self):
        return User.objects.select_related('profile').get(id=self.request.user.id).profile
   
      
    def perform_update(self, Serializer):
        profile= self.get_object()
        if profile.user!= self.request.user:
            return Response("you can only edit own profile")
        Serializer.save()
        cache.delete(f"my_profile_{self.request.user.id}")#! deleted cache after update
        return Response({
            "message": "Profile updated successfully."
        }, status=status.HTTP_200_OK)
     