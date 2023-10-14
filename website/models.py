# Create your models here.
from django.contrib.gis.db import models

class Booking(models.Model):
    start_date = models.DateField()
    pincode = models.CharField(max_length=10)
    route = models.ForeignKey('navigation.Route', on_delete=models.PROTECT)
    customer = models.ForeignKey('Customer', null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey('Status', on_delete=models.PROTECT)
    tracker = models.ForeignKey('navigation.Tracker', on_delete=models.CASCADE, related_name='bookings')

    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    last_edited = models.DateTimeField(auto_now=True)


class Inns(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    coordinates = models.PointField(srid=4326)
    last_edited = models.DateTimeField(auto_now=True)


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    coordinates = models.PointField(srid=4326)
    last_edited = models.DateTimeField(auto_now=True)


class RestStop(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.PROTECT)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.PROTECT)
    status = models.ForeignKey('Status', on_delete=models.PROTECT)


class OvernightStay(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.PROTECT)
    inn = models.ForeignKey('Inns', on_delete=models.PROTECT)
    status = models.ForeignKey('Status', on_delete=models.PROTECT)


class Status(models.Model):
    status_code = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=255)
    deletable = models.BooleanField()
    assign_pin = models.BooleanField()