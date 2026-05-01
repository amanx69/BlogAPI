from rest_framework.routers import DefaultRouter
from .views import Postview ,CommentViewset
from django.urls import path


router= DefaultRouter()


router.register("comment",CommentViewset,basename="comment")
router.register("post",Postview,basename="post")

urlpatterns = router.urls


urlpatterns += [
    # path('comments/<str:post_id>/', commentview.as_view(), name='comment-list'),
]