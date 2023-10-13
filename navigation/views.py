from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.views.generic import View
from .models import Marker, LandMark


class GpsView(View):
    def get(self, request, *args, **kwargs):
        template_name = "gps.html"

        markers = Marker.objects.all()
        donkey_travel = LandMark.objects.filter(name='Donkey Travel').get()
        return render(request, template_name, {"markers": markers, "donkeytravel": donkey_travel})

    def post(self, request, log):
        pass


class RouteView(View):
    def get(self, request, *args, **kwargs):
        template_name = "routes.html"

        markers = Marker.objects.all()
        donkey_travel = LandMark.objects.filter(name='Donkey Travel').get()
        return render(request, template_name, {"markers": markers, "donkeytravel": donkey_travel})

    def post(self, request):
        try:
            data = request.body.decode('utf-8')
            # You can print the received data
            print(data)
            
            # Process and save the LineString data from the request
            # Your processing logic here

            # Return a JSON response to indicate success
            response_data = {'message': 'LineString data saved successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            # Handle any exceptions and return an error response
            response_data = {'error': str(e)}