from django.urls import path
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordChangeView

from website.views import (
    HomepageView, BookingDetailView,BookingUpdateView, 
    BookingDeleteView, MapView, AccountView, AccountDeleteView, 
    BookingCreateView, ChangeRouteView, DashboardView, BookingsView, 
    Map2View, RoutesView, StaffAccommodationsView, AccommodationsView, 
    DeleteAccommodationsView, ListAccommodationsView, CreateInnView,
    InnsUpdateView, InnDeleteView, CreateRestaurantView,
    RestaurantDeleteView, RestaurantUpdateView,RestStopCreateView, 
    OvernightStayCreateView, ReststopDetailView, OvernightDetailView,
    RestStopDeleteView, RestStopUpdateView, OvernightStayDeleteView,
    OvernightStayUpdateView
    )


urlpatterns = [
    path("", HomepageView.as_view(), name='index'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('booking/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    path("bookingcreate/", BookingCreateView.as_view(), name='bookingcreate'),
    path("bookings/", BookingsView.as_view(), name='bookings'),
    path('accommodations/', ListAccommodationsView.as_view(), name='list_accommodations'),
    path('create-inn/', CreateInnView.as_view(), name='create_inn'),
    path('update_inn/<int:pk>/', InnsUpdateView.as_view(), name='update_inn'),
    path('inn/<int:pk>/delete/', InnDeleteView.as_view(), name='inn_delete'),
    path('create-restaurant/', CreateRestaurantView.as_view(), name='create_restaurant'),
    path('update_restaurant/<int:pk>/', RestaurantUpdateView.as_view(), name='update_restaurant'),
    path('restaurant/<int:pk>/delete/', RestaurantDeleteView.as_view(), name='restaurant_delete'),
    path('reststop/create/', RestStopCreateView.as_view(), name='reststop_create'),
    path('reststop/<int:pk>/', ReststopDetailView.as_view(), name='reststop_detail'),
    path('overnightstay/<int:pk>/', OvernightDetailView.as_view(), name='overnightstay_detail'),
    path('overnightstay/create/', OvernightStayCreateView.as_view(), name='overnightstay_create'),
    path('overnightstay/<int:pk>/update/', OvernightStayUpdateView.as_view(), name='overnightstay_update'),
    path('overnightstay/<int:pk>/delete/', OvernightStayDeleteView.as_view(), name='overnightstay_delete'),
    path('reststop/<int:pk>/update/', RestStopUpdateView.as_view(), name='reststop_update'),
    path('reststop/<int:pk>/delete/', RestStopDeleteView.as_view(), name='reststop_delete'),
    path("map/", MapView.as_view(), name='map'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('account_delete/<int:pk>/', AccountDeleteView.as_view(), name='account_delete'),
    path('change-password/', PasswordChangeView.as_view(template_name='change_password.html', success_url=reverse_lazy('index')), name='password_change'),
    path("changeroute/", ChangeRouteView.as_view(), name='changeroute'),
    path("dashboard/", DashboardView.as_view(), name='dashboard'),
    path("map2/", Map2View.as_view(), name='map2'),
    path("routes/", RoutesView.as_view(), name='routes'),
]
