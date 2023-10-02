from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class GpsView(TemplateView):
    template_name = "gps.html"