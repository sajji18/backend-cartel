from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nick_name = models.CharField(max_length=255,blank=True, null=True)
    user_id = models.AutoField(primary_key=True)
    profile_pic = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField()

    USER_TYPES = (
        ('user', 'User'),
        ('club', 'Club'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

    def __str__(self):
        return f'{self.username}'
    
    def __repr__(self):
        return f'{self.first_name} {self.last_name}'