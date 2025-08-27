from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms

from .models import User, Apartment,message,Image


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1','password2', 'phone','isBuyer']


class FilterForm(forms.ModelForm):
    phone = forms.CharField(max_length=15)
    isBuyer = forms.BooleanField(required=False)
    class Meta:
        model = Apartment
        fields = ['price', 'floor','city']

class MassageForm(forms.ModelForm):
    class Meta:
        model = message
        fields = ['body','name','email']


class ApartmentForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Apartment
        fields = ['rooms', 'floor', 'houseNumber', 'street', 'neighborhood', 'city', 'price', 'brokerage', 'description']
