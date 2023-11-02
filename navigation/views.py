import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import Point
from django.db.models.deletion import ProtectedError


from .models import Route, Obstacle, Tracker
from website.models import Booking
from .serializers import TrackerSerializer, BookingSerializer

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
        if self.request.user.is_staff:
            template_name = "routes.html"
        else:
            template_name = "gps.html"
        
        bookings = self.receive_bookings(request)

        markers = []
        return render(request, template_name, {"markers": markers, "bookings": bookings})

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
    
    def receive_bookings(self, request):
        serializer = BookingSerializer()

        if request.user.is_staff:
            bookings = Booking.objects.all()
            data = serializer.serialize(bookings)

        else:
            # User is not staff, so retrieve their own bookings
            customer = request.user.customer
            bookings = Booking.objects.filter(customer=customer)
            data = serializer.serialize(bookings)
        
        return data   

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
        # Ensure the request data contains the necessary fields
        if 'latitude' in data and 'longitude' in data and 'date_placed' in data:
            latitude = data['latitude']
            longitude = data['longitude']
            date_placed = data['date_placed']
            if 'comment'in data:
                comment = data['comment']

            # Create a Point from the latitude and longitude
            point = Point(longitude, latitude, srid=4326)

            obstacle = Obstacle(
                marker=point,
                date_placed=date_placed,
            )
            if comment:
                    obstacle.description=comment
            obstacle.save()
            return JsonResponse({'message': 'Obstacle created successfully'})
        else:
            return JsonResponse({'message': 'Invalid request data'}, status=400)
    

class ListObstaclesView(View):
    def get(self, request):
        obstacles = Obstacle.objects.all()
        obstacle_data = []

        for obstacle in obstacles:
            obstacle_data.append({
                'id': obstacle.id,
                'latitude': obstacle.marker.y,
                'longitude': obstacle.marker.x,
                'date_placed': obstacle.date_placed,
                'comment': obstacle.description,
            })

        return JsonResponse({'obstacles': obstacle_data})

def remove_obstacle(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        marker_id = data.get('id')
        try:
            # Retrieve the marker based on its ID and delete it
            marker = Obstacle.objects.get(id=marker_id)
            marker.delete()
            return JsonResponse({'message': 'Marker deleted successfully'})
        except Obstacle.DoesNotExist:
            return JsonResponse({'message': 'Marker not found'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)


class ListRoutesView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve all routes from the database
        if self.request.user.is_staff:
            routes = Route.objects.all()
        else:
            booking_id = request.GET.get('id')
            if booking_id is not None:
                booking = Booking.objects.filter(id=booking_id).first()
                routes = [booking.route]

        # Prepare route data in GeoJSON format
        routes_data = {
            "type": "FeatureCollection",
            "features": []
        }

        for route in routes:
            # Assuming route.route.geojson is a valid GeoJSON string
            route_data = {
                "id": route.id,
                "type": "Feature",
                "geometry": route.route.geojson,  # Make sure route.route.geojson is a valid GeoJSON string
                "properties": {
                    "description": route.description,
                    "duration_in_days": route.duration_in_days
                }
            }
            routes_data["features"].append(route_data)

        # Return the route data as GeoJSON
        return JsonResponse(routes_data)


def list_carts(request):
    if request.user.is_staff:
        trackers = Tracker.objects.all()
    else:
        booking = get_object_or_404(Booking, id=request.GET.get('id'))
        tracker = get_object_or_404(Tracker, booking=booking)
        trackers = [tracker]
 
    serializer = TrackerSerializer()
    data = serializer.serialize(trackers)
    return JsonResponse(data, safe=False)


def remove_route(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        route_id = data.get('id')

        try:
            route = get_object_or_404(Route, id=route_id)
            route.delete() 
            return JsonResponse({'message': 'Route removed successfully'})
        except ProtectedError as e:
            return JsonResponse({'error': 'Cannot delete route due to related objects.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to remove route: ' + str(e)})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def move_tracker(request):
    data = json.loads(request.body)
    # Ensure the request data contains the necessary fields
    if 'latitude' in data and 'longitude' in data:
        latitude = data['latitude']
        longitude = data['longitude']
        print('first if')

        # Create a Point from the latitude and longitude
        point = Point(longitude, latitude, srid=4326)

        if 'bookingId' in data: 
            print('2nd if')

            booking = get_object_or_404(Booking, id=data['bookingId'])
            tracker = get_object_or_404(Tracker, booking=booking)

            tracker.location = point

            if tracker.save():
                return JsonResponse({'message': 'Tracker created successfully'})
            else:
                return JsonResponse({'message': 'Tracker could not be moved'})
    else:
        return JsonResponse({'message': 'Invalid request data'}, status=400)