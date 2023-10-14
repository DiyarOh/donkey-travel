from django.contrib.gis.db import models


class Route(models.Model):
    description = models.TextField(default='NoNameRoute')
    route = models.LineStringField()  # Assuming you want to store a route as a LineString
    duration_in_days = models.PositiveIntegerField(default=4) # LineStringField to store the coordinates

    def __str__(self):
        return self.description
    

class Tracker(models.Model):
    pincode = models.CharField(max_length=10)
    location = models.PointField(srid=4326)  # Store the geographic location as a PointField
    time = models.DateTimeField()
    booking = models.ForeignKey('website.Booking', on_delete=models.CASCADE, related_name='trackers')
