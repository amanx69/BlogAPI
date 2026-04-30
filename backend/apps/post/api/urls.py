from rest_framework.routers import DefaultRouter
from .views import Postview ,CommentViewset


router= DefaultRouter()


router.register("comment",CommentViewset,basename="comment")
router.register("post",Postview,basename="post")
urlpatterns = router.urls