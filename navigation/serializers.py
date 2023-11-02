# serializers.py

from django.core.serializers import base
from django.db import models

# Define a serializer class for the Tracker model
class TrackerSerializer(base.Serializer):
    def serialize(self, queryset, **options):
        data = []
        # Iterate over each Tracker object in the queryset
        for tracker in queryset:
            # Get the associated Booking object
            booking = tracker.booking
            # Create a dictionary representing the Tracker object
            data.append({
                'pincode': tracker.pincode,
                'location': {
                    'type': 'Point',
                    'coordinates': [tracker.location.x, tracker.location.y],
                },
                'time': tracker.time,
                'booking': str(booking),  # Use __str__ method to get name + date
            })
        # Return the serialized data as a list of dictionaries
        return data
    
# Define a serializer class for the Booking model
class BookingSerializer(base.Serializer):
    def serialize(self, queryset, **options):
        data = []
        # Iterate over each Booking object in the queryset
        for booking in queryset:
            # Create a dictionary representing the Booking object
            data.append({
                'id': booking.id,
                'start_date': booking.start_date,
                'route': booking.route,
                'booking': str(booking),  # Use __str__ method to get name + date
            })
        # Return the serialized data as a list of dictionaries
        return data