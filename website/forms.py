from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.gis import forms as gis_forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import Point


from .models import Customer, Booking, Inns
from navigation.models import Route
from .validators import validate_phonenumber



class CustomMapWidget(forms.Widget):
    def __init__(self, attrs=None, initial_lat=51.6514359606463, initial_lng=5.048809728652404, existing_lat=None, existing_lng=None):
        self.initial_lat = initial_lat
        self.initial_lng = initial_lng
        self.existing_lat = existing_lat
        self.existing_lng = existing_lng
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        if not value and self.existing_lat is not None and self.existing_lng is not None:
            value = f'POINT({self.existing_lng} {self.existing_lat})'

        return mark_safe(f"""
            <div id="map" style="width: 100%; height: 500px;"></div>
            <input type="hidden" name="{name}" id="{attrs['id']}" value="{value}">
            <script>
                var map = L.map('map').setView([{self.initial_lat}, {self.initial_lng}], 17);

                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 24,
                }}).addTo(map);

                var marker;
                
                if ('{self.existing_lat}' !== 'None' && '{self.existing_lng}' !== 'None') {{
                    marker = L.marker([{self.existing_lat}, {self.existing_lng}]).addTo(map);
                    marker.bindPopup('Current Location').openPopup();
                }}

                map.on('click', function(e) {{
                    if (marker) {{
                        map.removeLayer(marker);
                    }}
                    marker = L.marker(e.latlng).addTo(map);
                    marker.bindPopup('New Location').openPopup();

                    var wktPoint = 'POINT(' + e.latlng.lng + ' ' + e.latlng.lat + ')';
                    
                    document.getElementById("{attrs['id']}").value = wktPoint;
                }});
            </script>
        """)
    
class DateOnlyPickerWidget(forms.DateInput):
    input_type = 'date'

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True, validators=[EmailValidator])
    first_name = forms.CharField(label="First Name", max_length=100, required=True)
    last_name = forms.CharField(label="Last Name", max_length=100, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)
    password_verify = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True) 
    phone = forms.CharField(label="Phone", max_length=20, required=False, validators=[validate_phonenumber]) 

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        phone = cleaned_data.get("phone")
        password_verify = cleaned_data.get("password_verify")
        name = f"{first_name} {last_name}"

        # Check if password and password verification match
        if password != password_verify:
            raise forms.ValidationError("Passwords do not match. Please try again.")
        

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


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']


class InnsForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={'size': '30'}),
        label='Address'
    )
    coordinates = gis_forms.PointField(srid=4326, widget=CustomMapWidget(attrs={'map_width': 800, 'map_height': 500}))

    class Meta:
        model = Inns
        exclude = ['last_edited']

    def clean_coordinates(self):
        coordinates = self.cleaned_data['coordinates']

        if coordinates:
            lat = coordinates.y
            lng = coordinates.x

        return coordinates

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.coordinates = self.cleaned_data.get('coordinates')
        
        if commit:
            instance.save()
        
        return instance
    

class InnsUpdateForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={'size': '30'}),
        label='Address'
    )
    coordinates = gis_forms.PointField(
        srid=4326,
        widget=CustomMapWidget(attrs={'map_width': 800, 'map_height': 500})
    )

    class Meta:
        model = Inns
        exclude = ['last_edited']