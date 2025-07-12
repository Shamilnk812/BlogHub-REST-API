from django.db import models
from users.models import User

class Post(models.Model):
    """
    Model representing a blog post.
    Includes title, content, optional excerpt, publishing status, soft delete,
    and timestamps for creation and updates.
    """
    author = models.ForeignKey( User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True) #short summary
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) # Soft delete flag

    def __str__(self):
        return self.title