from django.urls import path
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordChangeView

from website.views import (
    HomepageView, BookingDetailView,BookingUpdateView, 
    BookingDeleteView, MapView, AccountView, AccountDeleteView, 
    BookingCreateView, ChangeRouteView, DashboardView, BookingsView, 
    Map2View, RoutesView, StaffAccommodationsView, AccommodationsView, 
    DeleteAccommodationsView, ListAccommodationsView, CreateInnView,
    InnsUpdateView, InnDeleteView,
    )


urlpatterns = [
    path("", HomepageView.as_view(), name='index'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('booking/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    path("bookingcreate/", BookingCreateView.as_view(), name='bookingcreate'),
    path("bookings/", BookingsView.as_view(), name='bookings'),
    path('list-inns/', ListAccommodationsView.as_view(), name='list_accommodations'),
    path('create-inn/', CreateInnView.as_view(), name='create_inn'),
    path('update_inn/<int:pk>/', InnsUpdateView.as_view(), name='update_inn'),
    path('inn/<int:pk>/delete/', InnDeleteView.as_view(), name='inn_delete'),
    path("map/", MapView.as_view(), name='map'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('account_delete/<int:pk>/', AccountDeleteView.as_view(), name='account_delete'),
    path('change-password/', PasswordChangeView.as_view(template_name='change_password.html', success_url=reverse_lazy('index')), name='password_change'),
    path("changeroute/", ChangeRouteView.as_view(), name='changeroute'),
    path("dashboard/", DashboardView.as_view(), name='dashboard'),
    path("map2/", Map2View.as_view(), name='map2'),
    path("routes/", RoutesView.as_view(), name='routes'),
    path("staffaccommodations/", StaffAccommodationsView.as_view(), name='staffaccommodations'),
    path("accommodations/", AccommodationsView.as_view(), name='accommodations'),
    path("deleteaccommodations/", DeleteAccommodationsView.as_view(), name='deleteaccommodations'),
]
