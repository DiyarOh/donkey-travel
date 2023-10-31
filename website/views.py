from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.contrib.gis.geos import GEOSGeometry

from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, View
from django.views.generic.edit import FormView, DeleteView, UpdateView, CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.db import transaction

from .forms import RegistrationForm, CustomLoginForm, BookingForm, BookingUpdateForm, AccountUpdateForm, InnsForm, InnsUpdateForm, RestaurantForm, RestaurantUpdateForm, OvernightStayForm, RestStopForm, RestStopUpdateForm, OvernightStayUpdateForm
from .models import Status, Booking, Customer, Inns, Restaurant, RestStop, OvernightStay
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
            try:
                # Try to create a new user
                with transaction.atomic():
                    user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
                    customer = Customer.objects.create(user=user, email=form.cleaned_data['email'], phone=form.cleaned_data['phone'], name=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']} ")
                return redirect('index') 
            except IntegrityError as e:
                if 'unique constraint "auth_user_username_key"' in str(e):
                    # Handle duplicate username error
                    error_message = "A user with this username already exists. Please choose a different username."
                    form.add_error('username', error_message)
                elif 'unique constraint "app_customer_email_key"' in str(e):
                    # Handle duplicate email error
                    error_message = "This email address is already registered. Please use a different email."
                    form.add_error('email', error_message)
                elif 'unique constraint "app_customer_phone_key"' in str(e):
                    # Handle duplicate phone number error
                    error_message = "This phone number is already registered. Please use a different phone number."
                    form.add_error('phone', error_message)
                return render(request, self.template_name, {'form': form})
        else:
            # Form validation errors: Display the form with errors
            return render(request, self.template_name, {'form': form})


class BookingsView(TemplateView):
    template_name = "bookings.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_staff:
            # User is staff, so retrieve all bookings
            bookings = Booking.objects.all()
            reststops = RestStop.objects.all()
            overnightstays = OvernightStay.objects.all()
        else:
            # User is not staff, so retrieve their own bookings
            customer = self.request.user.customer
            bookings = Booking.objects.filter(customer=customer)
            reststops = RestStop.objects.filter(booking__customer=customer)
            overnightstays = OvernightStay.objects.filter(booking__customer=customer)

        context = {
            'bookings': bookings,
            'reststops': reststops,
            'overnightstays': overnightstays,
        }
        return self.render_to_response(context)


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
            return redirect('bookings')

        return render(request, self.template_name, {'form': form})


    def get_success_url(self):
        return redirect('bookings')


class ChangeRouteView(TemplateView):
    template_name = "changeroute.html"


class DashboardView(TemplateView):
    template_name = "dashboard.html"


class Map2View(TemplateView):
    template_name = "map2.html"


class RoutesView(TemplateView):
    template_name = "routes.html"


class StaffAccommodationsView(TemplateView):
    template_name = "staffaccommodations.html"


class CreateBookingView(TemplateView):
    template_name = "createbooking.html"


class AccommodationsView(TemplateView):
    template_name = "accommodations.html"
    

class DeleteAccommodationsView(TemplateView):
    template_name = "deleteaccommodations.html"
    

class MapView(TemplateView):
    template_name = "map.html"


class AccountView(UpdateView):
    model = Customer
    form_class = AccountUpdateForm
    template_name = "account.html"

    def get_success_url(self):
        return reverse_lazy('account', kwargs={'pk': self.object.pk})


class AccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('logout')
    template_name = 'account_confirm_delete.html'



class CreateInnView(FormView):
    template_name = 'create_inn.html'

    def get(self, request):
        form = InnsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InnsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['coordinates'])
            inn = form.save(commit=False)
            inn.coordinates = GEOSGeometry(form.cleaned_data['coordinates'])
            inn.save()
            return redirect('list_accommodations')
        return render(request, self.template_name, {'form': form})
    

class InnsUpdateView(UpdateView):
    model = Inns
    form_class = InnsUpdateForm
    template_name = 'update_inn.html'
    success_url = reverse_lazy('list_accommodations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = self.get_object()
        if instance.coordinates:
            form.fields['coordinates'].widget.existing_lat = instance.coordinates.y
            form.fields['coordinates'].widget.existing_lng = instance.coordinates.x
        return form


class InnDeleteView(DeleteView):
    model = Inns
    success_url = reverse_lazy('list_accommodations')
    template_name = 'inn_confirm_delete.html'


class ListAccommodationsView(View):
    template_name = 'list_accommodations.html'

    def get(self, request):
        inns = Inns.objects.all()
        restaurants = Restaurant.objects.all()
        return render(request, self.template_name, {'inns': inns, 'restaurants': restaurants})


class CreateRestaurantView(FormView):
    template_name = 'create_restaurant.html'

    def get(self, request):
        form = RestaurantForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RestaurantForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['coordinates'])
            inn = form.save(commit=False)
            inn.coordinates = GEOSGeometry(form.cleaned_data['coordinates'])
            inn.save()
            return redirect('list_accommodations')
        return render(request, self.template_name, {'form': form})
    

class RestaurantUpdateView(UpdateView):
    model = Restaurant
    form_class = RestaurantUpdateForm
    template_name = 'update_restaurant.html'
    success_url = reverse_lazy('list_accommodations')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        instance = self.get_object()
        if instance.coordinates:
            form.fields['coordinates'].widget.existing_lat = instance.coordinates.y
            form.fields['coordinates'].widget.existing_lng = instance.coordinates.x
        return form


class RestaurantDeleteView(DeleteView):
    model = Restaurant
    success_url = reverse_lazy('list_accommodations')
    template_name = 'restaurant_confirm_delete.html'


    
class OvernightDetailView(DetailView):
    model = OvernightStay
    template_name = 'overnightstay_detail.html'


class ReststopDetailView(DetailView):
    model = RestStop
    template_name = 'reststop_detail.html'



class OvernightStayCreateView(CreateView):
    model = OvernightStay
    form_class = OvernightStayForm 
    template_name = 'overnightstay_form.html'

    def get_success_url(self):
        return reverse_lazy('bookings') 
    def form_valid(self, form):
        form.instance.booking.customer = self.request.user.customer
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user 
        return kwargs
class RestStopCreateView(CreateView):
    model = RestStop
    form_class = RestStopForm  
    template_name = 'reststop_form.html' 

    def get_success_url(self):
        return reverse_lazy('bookings')

    def form_valid(self, form):
        form.instance.booking.customer = self.request.user.customer
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs


class OvernightStayUpdateView(UpdateView):
    model = OvernightStay
    form_class = OvernightStayUpdateForm
    template_name = 'update_page.html'

    def get_success_url(self):
        return reverse_lazy('bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


class RestStopUpdateView(UpdateView):
    model = RestStop
    form_class = RestStopUpdateForm
    template_name = 'update_page.html'

    def get_success_url(self):
        return reverse_lazy('bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

class OvernightStayDeleteView(DeleteView):
    model = OvernightStay
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('bookings')


class RestStopDeleteView(DeleteView):
    model = RestStop
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('bookings')