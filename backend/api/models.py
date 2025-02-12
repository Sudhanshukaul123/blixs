from django.db import models
from django.utils import timezone
from datetime import timedelta
import re
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def validate_user_id(value):
    if not re.match(r'^[a-z0-9._]+$', value):  
        raise ValidationError("User ID can only contain lowercase letters, dots (.), and underscores (_).")

def validate_password(value):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', value):
        raise ValidationError(
            "Password must be at least 8 characters long and include one uppercase letter, one lowercase letter, one number, and one special character."
        )


# Create your models here. 
class User(models.Model):
    user_id = models.CharField(unique=True ,max_length=15, validators=[validate_user_id] , null=False , primary_key=True)
    username = models.CharField(max_length=20 , blank=False )
    password = models.CharField(max_length=80 ,  validators=[validate_password] , null=False)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=100 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)
    gender = models.CharField(
        max_length=1, 
        choices=[('M', 'Male'), ('F', 'Female'), ('P', 'Prefer not to say')],
        default='P' 
    )
    profile_pic = models.ImageField(upload_to="profile_pics/" , null=True , blank=True)

    def __str__(self):
        return self.username 


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="posts")
    caption = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)

    def __str__(self):
        return f"Post by {self.user.username}"

class PostImage(models.Model):
    post = models.ForeignKey(Post , on_delete= models.CASCADE , related_name="post_images")
    image = models.ImageField(upload_to="images/Post_pics")

    def __str__(self):
        return f"Image for Post {self.post.post_id}"


class Hashtags(models.Model):
    tag = models.CharField(max_length=100 , blank=False , primary_key=True)
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type","object_id") 
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)

    def __str__(self):
        return self.tag  

class Like(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE , related_name="likes")
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id') 
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together  = ('user', 'content_type' , 'object_id' ) # duplication preventer

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE , related_name="user_comment")
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id') 
    commented_text = models.CharField(max_length=200 , blank=False )
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)
    parent = models.ForeignKey('self' , blank=True , null=True ,on_delete=models.CASCADE)

    def __str__(self):
        if self.parent :
            return f"Reply to {self.parent.id} by {self.user.username}"

        return f"Commented {self.commented_text} on {self.content_object} by {self.user.username}"

class SavedPost(models.Model):
    post = models.ForeignKey(Post , on_delete= models.CASCADE , related_name="saved_posts") 
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="saved_posts")
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)

    class Meta:
        unique_together = ('post', 'user')  # duplication preventer

    def __str__(self):
        return f"{self.user.username} saved Post {self.post.post_id}"   

class Followers(models.Model):
    follower =  models.ForeignKey(User , on_delete= models.CASCADE , related_name="followers")
    following =  models.ForeignKey(User , on_delete= models.CASCADE , related_name="following")
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Followers"
        unique_together = ('follower', 'following')  # duplication preventer

    def __str__(self):
        return f"{self.follower.username} following {self.following.username}"

def default_expiry():
    return timezone.now() + timedelta(hours=24)

class Story(models.Model):
    story_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    image = models.ImageField(upload_to="images/story_pics/")
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return f"Story by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True , db_index=True)
    notification_type = models.CharField(max_length=50, choices=[
    ('INFO', 'info'),
    ('WARNING', 'Warning'),
    ('ERROR', 'Error'),
    ('SUCCESS', 'Success'),
    ], default='INFO')

    def __str__(self):
        return f"Notfication for {self.user.username}: {self.message}"
    
    def mark_as_read(self):
        """Mark the notification as read"""
        self.is_read = True
        self.save()

    @property
    def was_created_recently(self):
        """Property to check if notification was created recently (within 24 hours)"""
        return self.created_at >= timezone.now() - timezone.timedelta(days=1)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=299)
    content = models.TextField(blank=True,null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_edited = models.BooleanField(default=False)
    deleted_for_user = models.ManyToManyField(User,blank=True,related_name="deleted_message")
    is_draft = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    replied_to = models.ForeignKey('self',null=True, blank=True, on_delete=models.DO_NOTHING , related_name="replies")
    forward_from = models.ForeignKey('self',null=True, blank=True, on_delete=models.DO_NOTHING , related_name="forwards")
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

    def edit_message(self,new_content):
        self.content = new_content
        self.edited_at = timezone.now()
        self.is_edited = True
        self.save()
        return self.content
    def delete_for_user(self ,user):
        self.deleted_for_user.add(user)

    def delete_message(self, user, for_everyone=False):
        if for_everyone:
            self.content = "[This message was deleted]"
            self.save()
        else:
            self.deleted_for_user.add(user)