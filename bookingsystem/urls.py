from django.urls import path
from . import views


from django.urls import path
from .views import BookVenueView, VenueListView, VenueDetailView

urlpatterns = [
    path('book-venue/', BookVenueView.as_view(), name='book-venue'),
    path('venues/', VenueListView.as_view(), name='venue-list'),
    path('venues/<int:pk>/', VenueDetailView.as_view(), name='venue-detail'),
    # Other URLs for booking and venue management
]
