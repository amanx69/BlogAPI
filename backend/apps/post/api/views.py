
from rest_framework.viewsets import ModelViewSet

from .seriilizers.bookmarkserlizer import BookmarkSerlizer
from ..models import  Bookmark, Like, Post ,Comment
from rest_framework.permissions import  IsAuthenticated
from  .seriilizers.Postserlizers import PostCreateSerializer, PostListSerializer 
from .seriilizers.commentSerlizer import CommentSerlizer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from ..premission import IsAuthorOrRedaonly ,IsOwner
from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef

User= get_user_model()


#! post viewset
@method_decorator(ratelimit(key='user', rate='5/m', method='POST'), name='create') 
class Postview(ModelViewSet): 
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.select_related('user', 'user__profile', 'category').annotate(
            annotated_likes_count=Count('post_like', distinct=True),
            annotated_comments_count=Count('comments', distinct=True),
        )
        
        if user.is_authenticated:
            # Efficiently check if current user liked the post
            liked_by_user = Like.objects.filter(post=OuterRef('pk'), user=user)
            queryset = queryset.annotate(is_liked_by_user=Exists(liked_by_user))
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PostListSerializer
        return PostCreateSerializer
    
    def get_permissions(self):
        permission_map = {
        'create'  : [IsAuthenticated(),IsAuthenticated()],
        'destroy' : [IsAuthenticated(),IsOwner()],
        'update'  : [IsAuthenticated(),IsOwner()],
        }
        return permission_map.get(self.action,[IsAuthenticated()])
    
    #! create a post
    def  perform_create(self, Serializer): 
        Serializer.save(user=self.request.user)
        
        #! only user can update
    def perform_update(self, serializer):
        serializer.save()
        
    
    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if post.status == "published":
            return Response(
                {"detail": "Post is already published."},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.publish()
        return Response(
            {"detail": "Post published.", "published_at": post.published_at},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        if post.status == "draft":
            return Response(
                {"detail": "Post is already a draft."},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.status = "draft"
        post.published_at = None
        post.save(update_fields=['status', 'published_at'])
        return Response({"detail": "Post reverted to draft."}, status=status.HTTP_200_OK)
        #! only user can deleted
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
    #! give all current user post
    @action(detail=False,methods=["GET"],url_path="my_post")
    def get_my_post(self,request):
        post= Post.objects.filter(user= request.user)
        ser= self.get_serializer(post,many= True)
        return Response(ser.data)
    
    
    

      
    
    
#! comment viewset
class CommentViewset(ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class= CommentSerlizer
    
    
    def get_permissions(self):
        permission_map = {
        'create'  : [IsAuthenticated(),IsAuthenticated()],
        'destroy' : [IsAuthenticated(),IsOwner()],
        
        }
        return permission_map.get(self.action,[IsAuthenticated()])
    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'), name='create')
    def perform_create(self, serializer): 
        post_id = self.request.data.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

    def perform_destroy(self, instance):
      
        if instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete() 
    @action(detail=False,methods=["GET"],url_path="my_comment")
    def  get_my_comment(self,request):
        comment= Comment.objects.filter(user= request.user)
        ser= self.get_serializer(comment,many= True)
        return Response(ser.data)


               
#! class Like

class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
        
        return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
    
    
    
    
    
#! bookmake 
class BookmarkView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        bookmarks= Bookmark.objects.filter(user= request.user).select_related("post")
        print(bookmarks)
        ser= BookmarkSerlizer(bookmarks,many= True)
        return Response(ser.data,status=status.HTTP_200_OK)
    
    
    def post(self,request,post_id):
        
        post= get_object_or_404(Post,pk=post_id)
        bookmark, created= Bookmark.objects.get_or_create(post=post,user=request.user)
        if not created:
            bookmark.delete()
            return Response({"message":"bookmake removed",},status=status.HTTP_200_OK)
        return Response({"message":"bookmark add"},status=status.HTTP_201_CREATED)
        
  
        
        
        

