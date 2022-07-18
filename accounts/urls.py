
"""djangoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path( 'products/', views.products, name='products'),
    path('customer/<str:customer_id>', views.customer, name='customer'),
    path('create_customer/', views.createCustomer, name="create_customer"),
    path('update_order/<str:order_id>', views.updateOrder, name="update_order"),
    path('update_customer/<str:customer_id>', views.updateCustomer, name="update_customer"),
    path('delete_order/<str:order_id>', views.deleteOrder, name="delete_order"),
    path('place_order/<str:customer_id>', views.placeOrder, name="place_order"),
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('user', views.userPage, name='user'),
    path('settings', views.accountSettings, name="settings"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset_password_sent.html"),
         name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_password_confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_password_complete.html"),
         name="password_reset_complete"),
]
