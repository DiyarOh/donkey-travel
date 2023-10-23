from django.contrib import admin

from .models import Booking, Customer, Inns, Restaurant, RestStop, OvernightStay, Status

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'pincode', 'route', 'customer', 'status')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'last_edited')

@admin.register(Inns)
class InnsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'phone', 'coordinates', 'last_edited')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'email', 'phone', 'coordinates', 'last_edited')

@admin.register(RestStop)
class RestStopAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'restaurant', 'status')

@admin.register(OvernightStay)
class OvernightStayAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'inn', 'status')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_code', 'status', 'deletable', 'assign_pin')

