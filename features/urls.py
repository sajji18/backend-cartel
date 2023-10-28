from django.urls import path
from . import views

urlpatterns = [
    path('saved/<str:username>/', views.SavedPostsView.as_view(), name='saved-posts'),
    # path('registered/', views.RegisteredEventsView.as_view(), name='registered-events'),
    path('add-to-saved-posts/', views.AddToSavedPostsView.as_view(), name='add-to-saved-posts'),
    path('register-to-event/', views.RegisterToEventView.as_view(), name='register-to-event'),
]
