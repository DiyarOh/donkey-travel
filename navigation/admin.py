from django.contrib import admin
from .models import Marker
# Register your models here
class MarkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(Marker, MarkerAdmin)