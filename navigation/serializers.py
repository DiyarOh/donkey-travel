# serializers.py

from django.core.serializers import base
from django.db import models

class TrackerSerializer(base.Serializer):
    def serialize(self, queryset, **options):
        data = []
        for tracker in queryset:
            booking = tracker.booking
            data.append({
                'pincode': tracker.pincode,
                'location': {
                    'type': 'Point',
                    'coordinates': [tracker.location.x, tracker.location.y],
                },
                'time': tracker.time,
                'booking': str(booking),  # Use __str__ method to get name + date
            })
        return data