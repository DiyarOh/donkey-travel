from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from .models import Marker, LandMark


class GpsView(View):
    def get(self, request, *args, **kwargs):
        template_name = "gps.html"

        markers = Marker.objects.all()
        donkey_travel = LandMark.objects.filter(name='Donkey Travel').get()
        return render(request, template_name, {"markers": markers, "donkeytravel": donkey_travel})