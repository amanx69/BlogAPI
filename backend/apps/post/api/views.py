
from rest_framework.viewsets import ModelViewSet
from ..models import  Post ,Comment
from rest_framework.permissions import  IsAuthenticated
from  .seriilizers.Postserlizers import PostCreateSerializer 
from .seriilizers.commentSerlizer import CommentSerlizer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class Postview(ModelViewSet): 
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    
    def get_permissions(self):
        permission_map = {
        'create'  : [IsAuthenticated(),IsAuthenticated()],
        'destroy' : [IsAuthenticated(),IsAuthenticated()],
        'get_my_job' : [IsAuthenticated(),IsAuthenticated()],

        
        }
        return permission_map.get(self.action,[IsAuthenticated()])
    #! create a job
    def  perform_create(self, Serializer): 
        Serializer.save(user=self.request.user)
        
        #! only user can update
    def perform_update(self,Serializer):
        post= self.get_object()
        
        if post.user!= self.request.user:
            
            return Response("you can only edit own job")
        Serializer.save()
        #! only user can deleted
    def perform_destroy(self,instance):
        if instance.user!= self.request.user:
            return Response("you can only delete own job ")
        instance.is_deleted= True
        instance.save()
        return Response("deleted done",status.HTTP_200_OK)
    #! give all current user post
    @action(detail=False,methods=["GET"],url_path="my_post")
    def get_my_job(self,request):
        post= Post.objects.filter(user=request.user)
        ser= self.get_serializer(post,many= True)
        return Response(ser.data)
    
    


class CommentViewset(ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class= CommentSerlizer
    
    
    def get_permissions(self):
        permission_map = {
        'create'  : [IsAuthenticated(),IsAuthenticated()],
        'destroy' : [IsAuthenticated(),IsAuthenticated()],
        
        }
        return permission_map.get(self.action,[IsAuthenticated()])
    
    def  perform_create(self, Serializer,): 
        id= self.request.data.get("post_id")
        post= get_object_or_404(Post,pk= id)
        Serializer.save(user=self.request.user,post=post)
        
    def perform_destroy(self, instance):
      
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete() 
    
    
    
    
    
    
    
    
        
   