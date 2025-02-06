from django.db import models
import re
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def validate_user_id(value):
    if not re.match(r'^[a-z._]+$', value):  
        raise ValidationError("User ID can only contain lowercase letters, dots (.), and underscores (_).")

def validate_password(value):
    if not re.search(r'\d', value):  # Search for at least one digit
        raise ValidationError("Password must contain at least one number.")

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('P', 'Prefer not to say'),  # Added option
]

# Create your models here. 
class User(models.Model):
    user_id = models.CharField(unique=True ,max_length=15, validators=[validate_user_id] , null=False , primary_key=True)
    username = models.CharField(max_length=20 , blank=False )
    password = models.CharField(min_length=8 , max_length=80 ,  validators=[validate_password] , null=False)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=100 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES,
        default='P' 
    )
    profile_pic = models.ImageField(upload_to="profile_pics/" , null=True , default="backendz/api/Media/images/profile_pic/Default_pic.png")

    def __str__(self):
        return self.username  # Display name in admin/print


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="Post")
    caption = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username}"

class Post_Image(models.Model):
    post = models.ForeignKey(Post , on_delete= models.CASCADE , related_name="posts_image")
    image = models.ImageField(upload_to="images/Post_pics")

    def __str__(self):
        return f"Image for Post {self.post.post_id}"


class Hashtags(models.Model):   
    hash_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100 , blank=False )
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type","object_id") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag  

class like(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE , related_name="likes")
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id') 
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together  = ('user', 'content_type' , 'object_id' ) 

    def __str__(self):
        return f"{self.user.username} liked {self.content_object}"
    
class comments(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE , related_name="users_comment")
    content_type = models.ForeignKey(ContentType , on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id') 
    commented_text = models.CharField(max_length=200 , blank=False )
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey('self' , blank=True , null=True ,on_delete=models.CASCADE)

    def __str__(self):
        if self.parent :
            return f"Reply to {self.parent.id} by {self.user.username}"

        return f"Commented {self.commented_text} on {self.content_object} by {self.user.username}"

class saved_post(models.Model):
    post = models.ForeignKey(Post , on_delete= models.CASCADE , related_name="saved_posts") 
    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="saved_posts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user.username} saved Post {self.post.post_id}"