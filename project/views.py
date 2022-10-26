import json
import os

from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .utilis import *
# Create your views here.

def index(request):
    return render(request, 'main/index.html')


def about_us(request):
    return render(request, 'main/about_us.html')


def menu_cat(request):
    data = cartData(request)
    cartitems = data['cartitems']
    cat_menu = Category.objects.all()
    context = {'cat_menu': cat_menu, 'cartitems': cartitems}
    return render(request, 'main/menu.html', context)


def products(request):
    category = request.GET.get('category')

    if category:
        product = Product.objects.filter(category__name=category)
    else:
        product = Product.objects.all()
    data = cartData(request)
    cartitems = data['cartitems']
    context = {'products': product, 'category': category, 'cartitems': cartitems}
    return render(request, 'main/products.html', context)


def cart(request):
    data = cartData(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'main/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    data = cartData(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    users = User.objects.filter(username=request.user)
    print(os.getenv('PAYPAL_CLIENT_ID'))
    context = {'items': items, 'order': order, 'cartitems': cartitems, 'user': users, 'client_id': os.getenv('PAYPAL_CLIENT_ID')}
    return render(request, 'main/checkout.html', context)


def updateItems(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId:', productId)
    print('action:', action)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=request.user)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    orderitem.save()

    if orderitem.quantity == 0:
        orderitem.delete()

    return JsonResponse('Items was added', safe=False)


def sign_up_page(request):
    page = 'register'
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You're Successful Registered")
            return redirect('login')
    context = {'form': form, 'page': page}
    return render(request, 'user/sign_up_login.html', context)


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'user/sign_up_login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def process_order(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data['form']['total'])
    print(transaction_id)
    print('Data:', request.body)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            print(total == order.get_cart_total)
            print(order.complete)
            order.complete = True
            print(order.complete)
        order.save()
        DeliveryAddress.objects.create(user=request.user, order=order,
                                       address=data['form']['address'],
                                       state=data['form']['state'],
                                       city=data['form']['city'],
                                       zipcode=data['form']['zipcode'],
                                       )
    return JsonResponse('payment complete', safe=False)
