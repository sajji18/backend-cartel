from django.db import models
from authentication.models import User

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    POST_CHOICES  = (
        
    )

    def __str__(self):
        return f"Post by {self.user.username} at {self.date_posted}"

