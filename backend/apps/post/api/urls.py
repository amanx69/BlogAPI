from rest_framework.routers import DefaultRouter
from .views import Postview ,CommentViewset ,LikeView ,BookmarkView
from django.urls import path


router= DefaultRouter()


router.register("comment",CommentViewset,basename="comment")
router.register("post",Postview,basename="post")

urlpatterns = router.urls


urlpatterns += [
    path("like/<int:post_id>/",LikeView.as_view(), name='post_like'),
    path("bookmark/<int:post_id>/",BookmarkView.as_view(), name='post_bookmark'),

]
