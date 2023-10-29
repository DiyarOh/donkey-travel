from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer, Booking
from navigation.models import Route


class DateOnlyPickerWidget(forms.DateInput):
    input_type = 'date'

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="First Name", max_length=100, required=True)
    last_name = forms.CharField(label="Last Name", max_length=100, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)
    password_verify = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True) 
    phone = forms.CharField(label="Phone", max_length=20, required=False) 

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        phone = cleaned_data.get("phone")
        password_verify = cleaned_data.get("password_verify")

        # Check if password and password verification match
        if password != password_verify:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        # Create a User instance
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create a Customer instance
        customer = Customer(
            name=f"{first_name} {last_name}",
            email=email,
            phone=phone,
            password=password,
            user=user
        )
        customer.save()

        return cleaned_data


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'route']
        
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class BookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'route', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BookingUpdateForm, self).__init__(*args, **kwargs)

        if user and not user.is_staff:
            # Exclude the 'status' field for non-staff users
            self.fields.pop('status')
        else: 
            current_status = self.instance.status
            self.initial['status'] = current_status
            self.fields['status'].label_from_instance = lambda obj: obj.status
            self.fields['status'].to_field_name = 'status'

        self.fields['route'].choices = [(route.id, route) for route in Route.objects.all()]

        self.fields['start_date'].widget = DateOnlyPickerWidget()