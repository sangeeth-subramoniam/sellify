from django.db import models
from django.shortcuts import redirect, render
from .models import cart, order
from django.db.models import Sum
import datetime

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cart_home(request):

    user_cart = cart.objects.all().filter(cart_user = request.user , cart_status = "pending")
    sum = 0
    for items in user_cart:
        sum += items.cart_product.shop_product_cost
    print(user_cart)
    print(sum)
    
    context = {
        'user_cart' : user_cart,
        'cart_sum' : sum
    }

    return render(request, 'cart/cart_home.html', context)

@login_required
def place_order(request):

    #lets add all pdt to order_list

    user_cart = cart.objects.all().filter(cart_user = request.user , cart_status = "pending")
    sum = 0

    for items in user_cart:
        sum += items.cart_product.shop_product_cost

    print(user_cart)
    print(sum)

    current_time = datetime.datetime.now() 
    hours_added = datetime.timedelta(hours = 9)
    corrected_datetime = current_time + hours_added

    new_order = order.objects.create(
        created_by = request.user,
        created_at = corrected_datetime,
        order_status = "pending",
        order_cost = sum
    )
    
    for items in user_cart:
        print('adding ', items.cart_product)
        new_order.order_products.add(items.cart_product)
        items.cart_status = "Ordered"
        items.save()

    new_order.save()

    return redirect('cart:orderplaced')

@login_required
def view_orders(request):

    orders = order.objects.all().filter(created_by = request.user).order_by('-created_at')

    context = {
        'orders' : orders
    }

    return render(request, 'cart/orders.html' , context)

def orderplaced(request):
    print('orderplaced... redirecting to homepage ... ')
    return render(request, 'cart/orderplaced.html')

