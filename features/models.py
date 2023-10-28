from django.db import models

# Create your models here

class Feature(models.Model):
    username = models.CharField(max_length=100, unique=True)
    saved_posts = models.TextField(blank=True)  # Storing post IDs as comma-separated values
    registered_events = models.TextField(blank=True)  # Storing event names as comma-separated values

    def __str__(self):
        return self.username


