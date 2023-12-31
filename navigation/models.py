from django.contrib.gis.geos import Point
from django.contrib.gis.db import models


class Route(models.Model):
    description = models.TextField(default='NoNameRoute')
    route = models.LineStringField() 
    duration_in_days = models.PositiveIntegerField(default=4) 

    def __str__(self):
        return self.description
    

class Tracker(models.Model):
    pincode = models.CharField(max_length=10)
    location = models.PointField(srid=4326, default=Point(5.0453889387953135, 51.65060519815468))
    time = models.DateTimeField(auto_now=True)
    booking = models.ForeignKey('website.Booking',null=True, on_delete=models.CASCADE, related_name='trackers')


class Obstacle(models.Model):
    marker = models.PointField(srid=4326)  # Point field for the marker with the SRID 4326
    date_placed = models.DateField()  # Date when the obstacle is placed
    description = models.CharField(default="no description") #adds marker comment to database

    def __str__(self):
        return f"Obstacle placed on {self.date_placed}"
