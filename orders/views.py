from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import Cart
from products.models import Product
from django.contrib import messages
from .models import *

def add_to_cart(request, product_id):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    product = Product.objects.get(id=product_id)

    # check if already in cart
    cart_item = Cart.objects.filter(user_id=user_id, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Quantity updated in cart")
    else:
        Cart.objects.create(user_id=user_id, product=product, quantity=1)
        messages.success(request, "Item added to cart")

    return redirect(request.META.get('HTTP_REFERER', 'user_products'))




def view_cart(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=user_id)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'orders/cart.html', {'cart_items': cart_items,'total':total})





from django.shortcuts import get_object_or_404

def remove_from_cart(request, cart_id):

    if 'user_id' not in request.session:
        return redirect('login')

    item = get_object_or_404(Cart, id=cart_id)

    item.delete()

    return redirect('view_cart')

def increase_quantity(request, cart_id):

    item = Cart.objects.get(id=cart_id)
    item.quantity += 1
    item.save()

    return redirect('view_cart')
def decrease_quantity(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('view_cart')

from users.models import Address

from django.shortcuts import render, redirect
from users.models import Address
from products.models import Product
from .models import Cart, Order, OrderItem


def checkout(request):

    user_id = request.session.get('user_id')

    #check login
    if not user_id:
        return redirect('login')

    # get cart items
    cart_items = Cart.objects.filter(user_id=user_id)

    # prevent empty cart checkout
    if not cart_items:
        return redirect('user_products')

    # get saved addresses
    addresses = Address.objects.filter(user_id=user_id)

    # calculate total
    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    # handle POST
    if request.method == "POST":

        # NEW ADDRESS FIELDS
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        addr = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        # EXISTING ADDRESS
        address_id = request.POST.get('address_id')

        # PRIORITY → NEW ADDRESS
        if all([name, phone, addr, city, pincode]):
            # VALIDATIONS

         if not name.replace(" ", "").isalpha():

            messages.error(request, "Invalid name")
            return redirect('checkout')

         if not city.replace(" ", "").isalpha():

            messages.error(request, "Invalid city")
            return redirect('checkout')

         if not phone.isdigit() or len(phone) != 10:

            messages.error(request, "Invalid phone number")
            return redirect('checkout')

         if not pincode.isdigit() or len(pincode) != 6:

            messages.error(request, "Invalid pincode")
            return redirect('checkout')
            

         address = Address.objects.create(
                user_id=user_id,
                name=name,
                phone=phone,
                address=addr,
                city=city,
                pincode=pincode
            )

        # OTHERWISE USE EXISTING ADDRESS
        elif address_id:

            address = Address.objects.get(id=address_id)

        # NO ADDRESS PROVIDED
        else:

            return redirect('checkout')

        #  create order
        order = Order.objects.create(
            user_id=user_id,
            address=address,
            total_price=total
        )

        #  create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        #  clear cart
        cart_items.delete()

        #  redirect after order
        messages.success(request, "Order placed successfully!")
        return redirect('order_history')

    #  render checkout page
    return render(request, 'orders/checkout.html', {
        'addresses': addresses,
        'total': total
    })

def order_history(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    orders = Order.objects.filter(user_id=user_id).order_by('-id')

    return render(request, 'orders/order_history.html', {
        'orders': orders
    })

def cancel_order(request, order_id):

    order = Order.objects.get(id=order_id)

    if order.status == "Pending":
        order.status = "Cancelled"
        order.save()

    return redirect('order_history')

def order_detail(request, order_id):

    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items
    })
