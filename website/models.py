# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit():
        raise ValidationError('Phone number must contain only numeric characters.')


class Booking(models.Model):
    start_date = models.DateField()
    pincode = models.CharField(max_length=10)
    route = models.ForeignKey('navigation.Route', on_delete=models.PROTECT)
    customer = models.ForeignKey('Customer', null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey('Status', default=0, on_delete=models.PROTECT)
    tracker = models.ForeignKey('navigation.Tracker',null=True, on_delete=models.CASCADE, related_name='bookings')
    
    def __str__(self):
        if self.customer:
            return f"{self.start_date} {self.customer.name}"
        else:
            return f"{self.start_date}"

    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(null=True, max_length=20, validators=[validate_phone_number])
    last_edited = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)


class Inns(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    coordinates = models.PointField(srid=4326)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    coordinates = models.PointField(srid=4326)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RestStop(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.PROTECT)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.PROTECT)
    status = models.ForeignKey('Status',default=0, on_delete=models.PROTECT)


class OvernightStay(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.PROTECT)
    inn = models.ForeignKey('Inns', on_delete=models.PROTECT)
    status = models.ForeignKey('Status',default=0, on_delete=models.PROTECT)


class Status(models.Model):
    status_code = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=255)
    deletable = models.BooleanField()
    assign_pin = models.BooleanField()

    def __str__(self):
        return self.status
