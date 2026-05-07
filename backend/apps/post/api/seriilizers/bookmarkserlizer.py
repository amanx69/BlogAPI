from rest_framework import serializers
from .Postserlizers import PostDetailSerializer
from apps.Profile.api.serlizer import ProfileSerlizer
from ...models import Bookmark




class BookmarkSerlizer(serializers.ModelSerializer):
    post= PostDetailSerializer(read_only= True)
    user= ProfileSerlizer(read_only= True)
    class Meta:
        model= Bookmark
        fields= ["id","post","user"]
        
        
