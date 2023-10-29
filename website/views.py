from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy

from .forms import RegistrationForm, CustomLoginForm, BookingForm, BookingUpdateForm  
from .models import Status, Booking
from navigation.models import Tracker

def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


class HomepageView(TemplateView):
    template_name = "index.html"


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = CustomLoginForm 

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
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form}) 
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return redirect('index') 


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'


class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingUpdateForm
    template_name = 'booking_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('booking_detail', kwargs={'pk': self.object.pk})

class BookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy('your_bookings_list_view')
    template_name = 'booking_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('bookings')


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


class DashboardView(TemplateView):
    template_name = "dashboard.html"


class BookingsView(TemplateView):
    template_name = "bookings.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_staff:
            # User is staff, so retrieve all bookings
            bookings = Booking.objects.all()
        else:
            # User is not staff, so retrieve their own bookings
            customer = self.request.user.customer
            bookings = Booking.objects.filter(customer=customer)
        
        context = {'bookings': bookings}
        return self.render_to_response(context)


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