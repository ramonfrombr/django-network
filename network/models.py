from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class UserFollowing(models.Model):
    user = models.ForeignKey("User", related_name="following",  on_delete=models.CASCADE)
    following_user = models.ForeignKey("User", related_name="followers",  on_delete=models.CASCADE)
    #created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'following_user'),)

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey("User", related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", related_name="comments",  on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = (('user', 'post'),)



