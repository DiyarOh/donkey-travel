from django.urls import path
from website.views import HomepageView, LoginView, RegisterView, BookingsView, MapView, AccountView, AccountLoginView, BookingCreateView, Bookings2View, ChangeRouteView, GuestDashboardView, GuestBookingsView, Map2View, RoutesView, StaffAccommodationsView, StaffBookingsView, StaffDashboardView, CreateBookingView, AccommodationsView, DeleteAccommodationsView
urlpatterns = [
    path("", HomepageView.as_view(), name='index'),
    path("login/", LoginView.as_view(), name='login'),
    path("register/", RegisterView.as_view(), name='register'),
    path("bookings/", BookingsView.as_view(), name='bookings'),
    path("map/", MapView.as_view(), name='map'),
    path("account/", AccountView.as_view(), name='account'),
    path("accountlogin/", AccountLoginView.as_view(), name='accountlogin'),
    path("bookingcreate/", BookingCreateView.as_view(), name='bookingcreate'),
    path("bookings2/", Bookings2View.as_view(), name='bookings2'),
    path("changeroute/", ChangeRouteView.as_view(), name='changeroute'),
    path("guestdashboard/", GuestDashboardView.as_view(), name='guestdashboard'),
    path("guestbookings/", GuestBookingsView.as_view(), name='guestbookings'),
    path("map2/", Map2View.as_view(), name='map2'),
    path("routes/", RoutesView.as_view(), name='routes'),
    path("staffaccommodations/", StaffAccommodationsView.as_view(), name='staffaccommodations'),
    path("staffbookings/", StaffBookingsView.as_view(), name='staffbookings'),
    path("staffdashboard/", StaffDashboardView.as_view(), name='staffdashboard'),
    path("createbooking/", CreateBookingView.as_view(), name='createbooking'),
    path("accommodations/", AccommodationsView.as_view(), name='accommodations'),
    path("deleteaccommodations/", DeleteAccommodationsView.as_view(), name='deleteaccommodations'),
]
