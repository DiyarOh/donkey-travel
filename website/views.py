from django.shortcuts import render

from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = "index.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegisterView(TemplateView):
    template_name = "register.html"


class BookingsView(TemplateView):
    template_name = "bookings.html"


class MapView(TemplateView):
    template_name = "map.html"


class AccountView(TemplateView):
    template_name = "account.html"


class AccountLoginView(TemplateView):
    template_name = "accountlogin.html"


class BookingCreateView(TemplateView):
    template_name = "bookingcreate.html"


class Bookings2View(TemplateView):
    template_name = "bookings2.html"


class ChangeRouteView(TemplateView):
    template_name = "changeroute.html"


class GuestDashboardView(TemplateView):
    template_name = "guestdashboard.html"


class GuestBookingsView(TemplateView):
    template_name = "guestbookings.html"


class Map2View(TemplateView):
    template_name = "map2.html"


class RoutesView(TemplateView):
    template_name = "routes.html"


class StaffAccommodationsView(TemplateView):
    template_name = "staffaccommodations.html"


class StaffBookingsView(TemplateView):
    template_name = "staffbookings.html"


class StaffDashboardView(TemplateView):
    template_name = "staffdashboard.html"


class CreateBookingView(TemplateView):
    template_name = "createbooking.html"


class AccommodationsView(TemplateView):
    template_name = "accommodations.html"
    

class DeleteAccommodationsView(TemplateView):
    template_name = "deleteaccommodations.html"