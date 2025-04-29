from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class User(AbstractUser):
    pass

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner} posted {self.body}"
    
    class Meta:
        ordering = ["-created_at"]
        
class Follow(models.Model):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} started to follow {self.followee} on {self.created_at}"
    
    class Meta:
        unique_together = ("followee", "follower")
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(followee=F("follower")),
                name="not_same",
            )
        ]