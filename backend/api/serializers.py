from rest_framework import serializers
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    hashtags = serializers.SerializerMethodField()
    views = serializers.IntegerField(default=0)  # Assuming views are tracked elsewhere

    class Meta:
        model = Post
        fields = ['post_id', 'user', 'caption', 'created_at', 'likes_count', 'comments_count', 'hashtags', 'views']
        
    def get_likes_count(self, obj):
        return Like.objects.filter(content_type__model='post', object_id=obj.post_id).count()
    
    def get_comments_count(self, obj):
        return Comment.objects.filter(content_type__model='post', object_id=obj.post_id).count()
    
    def get_hashtags(self, obj):
        return [tag.tag for tag in Hashtags.objects.filter(object_id=obj.post_id)]

class HashtagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtags
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = "__all__"

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = "__all__"

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"