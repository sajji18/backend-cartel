from rest_framework import serializers
from .models import Venue, Booking

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'capacity']  # Include more fields if needed


from .models import Venue

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'club', 'venue', 'date']  # Add more fields as needed
