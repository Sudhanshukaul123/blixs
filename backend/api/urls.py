from django.urls import path , include 
from rest_framework.routers import DefaultRouter 
from api.views import *


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)
router.register(r'hashtags', HashtagsViewSet)
router.register(r'like', LikeViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'savedPost', SavedPostViewSet)
router.register(r'followers', FollowersViewSet)
router.register(r'story', StoryViewSet)
router.register(r'notification', NotificationViewSet)
router.register(r'message', MessageViewSet)

urlpatterns = [
    path('',include(router.urls)),
]