

# Create your models here.

from django.db import models
from authentication.models import User  # Import User model from your authentication app


class Venue(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.name} with id : {self.id}'


class Booking(models.Model):
    club = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField()
    # Other fields for additional booking details

    def __str__(self):
        return f'Booked by {self.club} for {self.date}'

    