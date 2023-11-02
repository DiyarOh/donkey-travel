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
        """
        Retrieves a list of bookings and renders the appropriate template based on the user's role.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The rendered HTTP response.
        """
        if self.request.user.is_staff:
            template_name = "routes.html"
        else:
            template_name = "gps.html"
        
        bookings = self.receive_bookings(request)

        markers = []
        return render(request, template_name, {"markers": markers, "bookings": bookings})

    def post(self, request):
        """
        Handles the HTTP POST request.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: The JSON response containing the message 'Request handled successfully.'
        """
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
        """
        Receive bookings based on the given request.

        Parameters:
            request (Request): The request object containing user information.

        Returns:
            str: The serialized data of the bookings.
        """
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
        """
        Creates a route based on the given request data.

        Args:
            request (HttpRequest): The HTTP request object containing the route data.

        Returns:
            JsonResponse: A JSON response indicating the success or failure of the route creation.
        """
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
        """
        Create an obstacle based on the provided request data.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating the result of the operation.
                - If the request data is valid, returns a JSON response with the message 'Obstacle created successfully'.
                - If the request data is invalid, returns a JSON response with the message 'Invalid request data' and a status code of 400.
        """
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
        """
        Retrieves all obstacles from the database and returns them as a JSON response.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing the obstacle data.
        """
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
    """
    Removes an obstacle based on the given request.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response indicating the result of the operation.
            - If the obstacle is successfully deleted, returns a JSON response with the message 'Marker deleted successfully'.
            - If the obstacle is not found, returns a JSON response with the message 'Marker not found' and a status code of 400.
            - If the request is invalid, returns a JSON response with the message 'Invalid request' and a status code of 400.
    """
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
        """
        Retrieves routes from the database and prepares route data in GeoJSON format.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: The route data in GeoJSON format.
        """
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
    """
    Retrieves a list of carts based on the given request.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the serialized data of the trackers.
    """
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
    """
    Removes a route based on the provided route ID.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the result of the route removal.
            - If the route is removed successfully, returns a JSON response with the message 'Route removed successfully'.
            - If the route cannot be deleted due to related objects, returns a JSON response with the error message 'Cannot delete route due to related objects.' and status code 400.
            - If an exception occurs during the removal process, returns a JSON response with the error message 'Failed to remove route: {error_message}' and status code 400.
            - If an invalid request method is used, returns a JSON response with the error message 'Invalid request method' and status code 400.
    """
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
    """
    Moves the tracker to the specified latitude and longitude.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response indicating the success or failure of the tracker move.
    """
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