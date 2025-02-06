from django.db import models
import re
from django.core.exceptions import ValidationError

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
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"Image for Post {self.post.post_id}"


class Hashtags(models.Model):   
    hash_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100 , blank=False )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag  
    
class Post_hashtags(models.Model):
    post_id = models.ForeignKey(Post, on_delete= models.CASCADE , related_name="posts_hashtag")
    hash_id = models.ForeignKey(Hashtags, on_delete= models.CASCADE , related_name="hashtag_id")

    def __str__(self):
        return f"Hashtag {self.hash_id.tag} for Post {self.post_id.post_id}"
    
class likes(models.Model):
    like_id = models.AutoField(primary_key=True)
    liked = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete= models.CASCADE , related_name="user_like")
    post_id = models.ForeignKey(Post, on_delete= models.CASCADE , related_name="post_liked")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user_id.username} on Post {self.post_id.post_id}"