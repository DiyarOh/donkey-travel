import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import LineString


from .models import Route

# Create your views here.
from django.views.generic import View


class GpsView(View):
    def get(self, request, *args, **kwargs):
        template_name = "gps.html"

        markers = []
        return render(request, template_name, {"markers": markers})

    def post(self, request, log):
        pass


class RouteView(View):
    def get(self, request, *args, **kwargs):
        template_name = "routes.html"

        markers = []
        return render(request, template_name, {"markers": markers})

    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body)
            action = data.get('action')

            print(data)

        if action == 'create':
            self.create(request)
        
        elif action == 'read':
            pass

        elif action == 'update':
            pass

        elif action == 'delete':
            pass
        return JsonResponse({'message': 'Request handled successfully.'})
    
    def create(self, request):
        data = json.loads(request.body)
        
        if data['type'] == 'LineString':
            # Extract the necessary data from the JSON payload
            description = data.get('description')
            duration_in_days = data.get('duration')
            route_coordinates = data['coordinates']['coordinates']

            # Create a LineString from the coordinates
            route = GEOSGeometry(json.dumps({
                "type": "LineString",
                "coordinates": route_coordinates
            }), srid=4326)

            # Create a new Route record
            route_record = Route(
                description=description,
                route=route,
                duration_in_days=duration_in_days
            )

            route_record.save()
            return JsonResponse({'message': 'Route created successfully'})
        else:
            return JsonResponse({'message': 'Invalid request type'}, status=400)