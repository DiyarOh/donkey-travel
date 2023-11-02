from django.urls import path
from navigation.views import GpsView, RouteView, ListObstaclesView, remove_obstacle, ListRoutesView, list_carts, remove_route, move_tracker

urlpatterns = [
    path("map/", GpsView.as_view(), name='map'),
    path("routes/", RouteView.as_view(), name='routes'),
    path('list-obstacles/', ListObstaclesView.as_view(), name='list_obstacles'),
    path('remove_obstacle/', remove_obstacle, name='remove_obstacle'),
    path('list-routes/', ListRoutesView.as_view(), name='list_routes'),
    path('list_carts', list_carts, name='list_carts'),
    path('remove_route', remove_route, name='remove_route'),
    path('move_tracker', move_tracker, name='move_tracker'),
    



]
