from django.urls import path
from navigation.views import GpsView, RouteView

urlpatterns = [
    path("map/", GpsView.as_view(), name='map'),
    path("routes/", RouteView.as_view(), name='routes'),
]
