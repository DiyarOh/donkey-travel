from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import Marker


class GpsView(TemplateView):
    
    def get(request, *args, **kwargs):
        template_name = "gps.html"
        markers = Marker.objects.all()
        return render(request, template_name, {"markers": markers})