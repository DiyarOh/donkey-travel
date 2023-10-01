from django.contrib import admin
from .models import Location  # Replace 'Location' with your model's name

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'point')
    search_fields = ('name',)
    list_filter = ('name',)

# Register your model with the admin site
admin.site.register(Location, LocationAdmin)
