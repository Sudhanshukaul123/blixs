from rest_framework import viewsets 
from api.models import *
from api.serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

class HashtagsViewSet(viewsets.ModelViewSet):
    queryset = Hashtags.objects.all()
    serializer_class = HashtagsSerializer
    

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

class SavedPostViewSet(viewsets.ModelViewSet):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer
    

class FollowersViewSet(viewsets.ModelViewSet):
    queryset = Followers.objects.all()
    serializer_class = FollowersSerializer
    

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    