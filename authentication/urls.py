from django.urls import path
from . import views

urlpatterns = [
    path('users-list/', views.UserListView.as_view()),
]
  