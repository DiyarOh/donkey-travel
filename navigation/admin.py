from django.contrib import admin
from .models import Route, Tracker

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'route', 'duration_in_days')

@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('id', 'pincode', 'location', 'time', 'booking')