from django.urls import path
from website.views import HomepageView, BookingDetailView,BookingUpdateView, BookingDeleteView, MapView, AccountView, AccountLoginView, BookingCreateView, ChangeRouteView, DashboardView, BookingsView, Map2View, RoutesView, StaffAccommodationsView, AccommodationsView, DeleteAccommodationsView


urlpatterns = [
    path("", HomepageView.as_view(), name='index'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('booking/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    path("bookingcreate/", BookingCreateView.as_view(), name='bookingcreate'),
    path("bookings/", BookingsView.as_view(), name='bookings'),
    path("map/", MapView.as_view(), name='map'),
    path("account/", AccountView.as_view(), name='account'),
    path("accountlogin/", AccountLoginView.as_view(), name='accountlogin'),
    path("changeroute/", ChangeRouteView.as_view(), name='changeroute'),
    path("dashboard/", DashboardView.as_view(), name='dashboard'),
    path("map2/", Map2View.as_view(), name='map2'),
    path("routes/", RoutesView.as_view(), name='routes'),
    path("staffaccommodations/", StaffAccommodationsView.as_view(), name='staffaccommodations'),
    path("accommodations/", AccommodationsView.as_view(), name='accommodations'),
    path("deleteaccommodations/", DeleteAccommodationsView.as_view(), name='deleteaccommodations'),
]
