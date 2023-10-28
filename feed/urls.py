from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.PostList.as_view(), name='post-list'),
    path('feed/create/', views.PostCreate.as_view(), name='post-create'),
]
