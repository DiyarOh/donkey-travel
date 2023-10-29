from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import RegistrationForm, CustomLoginForm, BookingForm
from .models import Status
from navigation.models import Tracker


def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


class HomepageView(TemplateView):
    template_name = "index.html"


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = CustomLoginForm  # Set your custom form

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # Add additional context data as needed
        context['custom_data'] = "Additional Data"
        return render(request, self.template_name, context)


class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = ""

    def get(self, request):
        form = RegistrationForm()  # Create an instance of the RegistrationForm
        return render(request, self.template_name, {'form': form}) 
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return redirect('index') 


class BookingsView(FormView):
    template_name = "bookings.html"


class MapView(TemplateView):
    template_name = "map.html"


class AccountView(TemplateView):
    template_name = "account.html"


class AccountLoginView(TemplateView):
    template_name = "accountlogin.html"


class BookingCreateView(FormView):
    template_name = "bookingcreate.html"
    
    def get (self, request):
        form = BookingForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = self.request.user.customer
            default_status = Status.objects.get(status_code=0)
            booking.status = default_status
            booking.save()
            tracker = Tracker.objects.create(pincode='0000', booking=booking)
            tracker.save()
            booking.tracker = tracker
            booking.save()
            return redirect('index')

        return render(request, self.template_name, {'form': form})


    def get_success_url(self):
        return redirect('index')

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