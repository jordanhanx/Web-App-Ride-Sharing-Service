from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import Driver, Ride, Sharer


#######################################################################################
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "username"}))
    password = forms.CharField(max_length=512, label="Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "password"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class PswdChgForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old password",
                                   max_length=500, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="New password",
                                    max_length=500, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="New password confirmation",
                                    max_length=500, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["old_password ", "new_password1", "new_password2"]


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["user", "first_name", "last_name", "plate_nubmer",
                  "veh_type", "capacity", "manufacturer", "vehicle_info"]
        widgets = {
            "user": forms.HiddenInput,
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "plate_nubmer": forms.TextInput(attrs={"class": "form-control"}),
            "veh_type": forms.Select(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "manufacturer": forms.TextInput(attrs={"class": "form-control"}),
            "vehicle_info": forms.TextInput(attrs={"class": "form-control"}),
        }


class RideRequestForm(forms.ModelForm):

    class Meta:
        model = Ride
        fields = ["owner", "start_point", "destination", "req_arrival_time",
                  "veh_type", "passengers", "is_shared", "special_request"]
        widgets = {
            "owner": forms.HiddenInput,
            "start_point": forms.TextInput(attrs={"class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "req_arrival_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control", "placeholder": "2023-01-01 00:00:00"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "veh_type": forms.Select(attrs={"class": "form-control"}),
            "passengers": forms.NumberInput(attrs={"class": "form-control"}),
            "is_shared": forms.Select(attrs={"class": "form-control"}),
            "special_request": forms.TextInput(attrs={"class": "form-control"}),
        }


class SharerForm(forms.ModelForm):
    ride_id = forms.IntegerField(
        label=" ", widget=forms.HiddenInput)

    class Meta:
        model = Sharer
        fields = ["party_passengers", "ride_id"]
        widgets = {
            "party_passengers": forms.NumberInput(attrs={"class": "form-control"}),
        }
