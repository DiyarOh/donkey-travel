from django.contrib import admin
from .models import Route, Tracker, Obstacle

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'route', 'duration_in_days')

@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('id', 'pincode', 'location', 'time', 'booking')

@admin.register(Obstacle)
class ObstacleAdmin(admin.ModelAdmin):
    list_display = ('id', 'marker', 'date_placed')