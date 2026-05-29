from django.shortcuts import render,redirect
from .models import *

# Create your views here.
from django.db.models import Sum
from django.utils.timezone import now
from orders.models import Order
from products.models import Product


from django.utils import timezone
from datetime import timedelta




def owner_dashboard(request):

    if 'owner_id' not in request.session:
        return redirect('login')

    total_orders = Order.objects.count()

    accepted_orders = Order.objects.filter(
        status='Accepted'
    )

    total_profit = sum(
        order.total_price for order in accepted_orders
    )

    now = timezone.now()

    monthly_orders = Order.objects.filter(
        created_at__month=now.month,
        created_at__year=now.year
    ).count()

    total_products = Product.objects.count()

    recent_orders = Order.objects.all().order_by(
        '-created_at'
    )[:5]

    context = {

        'total_orders': total_orders,
        'total_profit': total_profit,
        'monthly_orders': monthly_orders,
        'total_products': total_products,
        'recent_orders': recent_orders,
    }

    return render(
        request,
        'owner/dashboard.html',
        context
    )




def owner_orders(request):

    days = request.GET.get('days')

    orders = Order.objects.all().order_by('-created_at')

    if days == '7':
        start = timezone.now() - timedelta(days=7)
        orders = orders.filter(created_at__gte=start)

    elif days == '30':
        start = timezone.now() - timedelta(days=30)
        orders = orders.filter(created_at__gte=start)

    context = {
        'orders': orders
    }

    return render(
        request,
        'owner/orders.html',
        context
    )

def accept_order(request, order_id):

    order = Order.objects.get(id=order_id)
    order.status = "Accepted"
    order.save()

    return redirect('owner_orders')


def reject_order(request, order_id):

    order = Order.objects.get(id=order_id)
    order.status = "Rejected"
    order.save()

    return redirect('owner_orders')

from products.models import Product

def owner_products(request):

    if 'owner_id' not in request.session:
        return redirect('login')

    products = Product.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products
    })