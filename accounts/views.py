from django.shortcuts import render
from django.forms import inlineformset_factory
# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    total_orders = orders.count()
    dictionary = {"customers": customers, "orders": orders, "delivered_orders": delivered_orders,
                  "pending_orders": pending_orders,
                  "total_orders": total_orders
                  }

    return render(request, "accounts/index.html", dictionary)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
    # query a database for products
    items = Product.objects.all()
    # add a dictionary to render to enable using
    # products inside products
    return render(request, "accounts/products.html", {
        'products': items
    })


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def customer(request, customer_id):
    customer_obj = Customer.objects.get(id=customer_id)
    orders = customer_obj.order_set.all()
    total_orders = orders.count()
    order_filter = OrderFilter(request.GET, queryset=orders)
    orders =order_filter.qs  # qs-> queryset
    dictionary = {"customer": customer_obj, "orders": orders,
                  "total_orders": total_orders,
                  "order_filter": order_filter}
    return render(request, "accounts/customer.html", dictionary)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def updateOrder(request, order_id):
    order = Order.objects.get(id=order_id)
    update_form = OrderForm(instance=order)
    if request.method == 'POST':
        update_form = OrderForm( request.POST, instance=order)
        if update_form.is_valid():
            update_form.save()
            return redirect('/')

    dictionary = {"update_form": update_form}
    return render(request, "accounts/update_form.html", dictionary)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def deleteOrder(request, order_id):
    order = Order.objects.get( id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    dictionary = {"order": order}
    return render( request, "accounts/delete_form.html", dictionary)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    dictionary={'form': form}
    return render(request, "accounts/customer_form.html", dictionary)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def updateCustomer(request, customer_id):
    client = Customer.objects.get( id=customer_id)
    form = CustomerForm( instance=client)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return customer(request, customer_id)

    dictionary={'form': form}
    return render(request, "accounts/customer_update_form.html", dictionary)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def placeOrder(request, customer_id):
    # if we want more fields in form then we add extra value to inlineformset
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    client = Customer.objects.get(id=customer_id)
    # queryset=Order.objects.none()=> we are not showing already
    # created order in form
    formset = OrderFormSet(queryset=Order.objects.none(), instance=client)
    # form = OrderForm(initial={"customer": client})
    if request.method == "POST":
        # initial-> we initialize customer with client with this id
        formset = OrderFormSet(request.POST, instance=client)
        if formset.is_valid():
            formset.save()
            return customer(request, customer_id)

    dictionary = {"client": client, "formset": formset}
    return render(request, "accounts/place_order.html", dictionary)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "There are no such user")

    dictionary = {}
    return render(request, "accounts/login.html", dictionary)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created for ' + user.username)
            return redirect('login')

    dictionary = {"form": form}
    return render(request, "accounts/register.html", dictionary)


@login_required
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    pending_orders = orders.filter(status="Pending").count()
    delivered_orders = orders.filter(status="Delivered").count()
    dictionary = {"orders": orders, "delivered_orders": delivered_orders,
                  "pending_orders": pending_orders,
                  "total_orders": total_orders
                  }
    return render(request, 'accounts/user.html', dictionary)


@login_required
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)
    dictionary = {"user": user, "form": form}
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=user)
        # we are adding request.FILES because of profile picture
        if form.is_valid():
            form.save()

    return render(request, "accounts/account_settings.html", dictionary)
