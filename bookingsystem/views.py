from rest_framework import generics, status
from rest_framework.response import Response
from datetime import datetime, timedelta
from bookingsystem.models import Booking, Venue
from .serializer import BookingSerializer, VenueSerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

class BookVenueView(generics.CreateAPIView):
    serializer_class = BookingSerializer  # Assuming you've created a serializer for the Booking model

    def post(self, request, *args, **kwargs):
        print(request.data)
        current_user = self.request.user
        print(current_user.user_type)

        if current_user.user_type != 'club':
            return Response("You are not authorized to book venues.", status=403)

        venue_id = request.data.get('venue')
        date = request.data.get('date')

        if not venue_id and not date:
            return Response("Venue ID and date are required for booking.", status=400)

        # Check if the venue is available on the requested date
        try:
            requested_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response("Invalid date format. Please use YYYY-MM-DD.", status=400)

        try:
            venue = Venue.objects.get(id=venue_id)
        except ObjectDoesNotExist:
            return Response("The requested venue does not exist.", status=status.HTTP_404_NOT_FOUND)

        conflicting_bookings = Booking.objects.filter(venue=venue, date=requested_date)
        if conflicting_bookings.exists():
            # Venue already booked on the requested date
            # Logic for suggesting alternative dates

            # Suggest alternative dates within the next 7 days
            alternative_dates = self.find_alternative_dates(venue, requested_date, days=7)

            if alternative_dates:
                return Response({
                    "message": "Venue is already booked on the requested date.",
                    "suggested_dates": [date.strftime('%Y-%m-%d') for date in alternative_dates]
                }, status=409)
            else:
                return Response("No available dates found within the next 7 days.", status=409)
        else:
            # Venue is available, create the booking
            booking = Booking.objects.create(
                club=current_user, # Assuming 'username' is the club's name field in the User model
                venue=venue,
                date=requested_date
            )
            return Response("Venue booked successfully for the requested date.", status=201)

    def find_alternative_dates(self, venue, requested_date, days):
        available_dates = []
        for i in range(days):
            new_date = requested_date + timedelta(days=i)
            conflicting_bookings = Booking.objects.filter(venue=venue, date=new_date)
            if not conflicting_bookings.exists():
                available_dates.append(new_date)
                # Suggest multiple available dates if found
                if len(available_dates) >= 3:
                    break
        return available_dates
    

class VenueListView(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueDetailView(generics.RetrieveAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    lookup_field = 'pk'
    
