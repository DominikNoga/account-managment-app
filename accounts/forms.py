from django.forms import ModelForm
from .models import Order, Customer
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderForm(ModelForm):
    class Meta:
        model = Order
        # model that we are referring to
        fields = '__all__'
        # create form with all fields of order


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'username', 'email', 'phone', 'profile_pic']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
