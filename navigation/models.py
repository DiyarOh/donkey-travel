from django.contrib.gis.db import models

class Marker(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    

class LandMark(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()


class Route(models.Model):
    name = models.CharField(max_length=100)  # Name of the route
    coordinates = models.LineStringField()  # LineStringField to store the coordinates

    def __str__(self):
        return self.name