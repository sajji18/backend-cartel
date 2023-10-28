from django.urls import path
from . import views

urlpatterns = [
    path('feed/user/<str:username>/', views.PostList.as_view(), name='post-list'),
    # path('feed/club/<str:username>/', views.PostCreate.as_view(), name='post-create'),
    path('feed/club/<str:username>/', views.UserPostsView.as_view(), name='user-posts')
    
]
