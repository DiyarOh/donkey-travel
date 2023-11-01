import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import Point


from .models import Route, Obstacle

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

        if action == 'create-route':
            self.create_route(request)
        
        elif action == 'create-obstacle':
            print('Imm here')
            self.create_obstacle(request)

        elif action == 'update':
            pass

        elif action == 'delete':
            pass
        return JsonResponse({'message': 'Request handled successfully.'})
    
    def create_route(self, request):
        data = json.loads(request.body)
        
        if data['type'] == 'LineString':
            description = data.get('description')
            duration_in_days = data.get('duration')
            route_coordinates = data['coordinates']['coordinates']

            route = GEOSGeometry(json.dumps({
                "type": "LineString",
                "coordinates": route_coordinates
            }), srid=4326)

            route_record = Route(
                description=description,
                route=route,
                duration_in_days=duration_in_days
            )

            route_record.save()
            return JsonResponse({'message': 'Route created successfully'})
        else:
            return JsonResponse({'message': 'Invalid request type'}, status=400)

    def create_obstacle(self, request):
        data = json.loads(request.body)
        print("Im not useless yet")
        # Ensure the request data contains the necessary fields
        if 'latitude' in data and 'longitude' in data and 'date_placed' in data:
            latitude = data['latitude']
            longitude = data['longitude']
            date_placed = data['date_placed']
            if 'comment'in data:
                comment = data['comment']

            # Create a Point from the latitude and longitude
            point = Point(longitude, latitude, srid=4326)

            # Create a new Obstacle record

            obstacle = Obstacle(
                marker=point,
                date_placed=date_placed,
            )
            if comment:
                    obstacle.description=comment
            print("EUREKA")
            obstacle.save()
            return JsonResponse({'message': 'Obstacle created successfully'})
        else:
            return JsonResponse({'message': 'Invalid request data'}, status=400)