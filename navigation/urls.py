from django.urls import path
from navigation.views import GpsView

urlpatterns = [
    path("", GpsView.as_view(), name='gps'),
]