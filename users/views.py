from django.shortcuts import render,redirect

# Create your views here.
from .models import *

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create(username=username, password=password)
        return redirect("login")

    return render(request, "users/register.html")


from users.models import User
from owner.models import Owner
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check Owner first
        owner = Owner.objects.filter(username=username, password=password).first()
        if owner:
            request.session['owner_id'] = owner.id
            return redirect("owner_dashboard")

        # Check User
        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect("user_home")
        else:
            # ❌ WRONG LOGIN
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")





def user_home(request):
    if not request.session.get('user_id'):
        return redirect('login')

    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    user_id = request.session.get('user_id')     

    wishlist_items = Wishlist.objects.filter(
        user_id=user_id
    ).values_list('product_id', flat=True)    

    return render(request, 'users/home.html', {
        'products': products,
        'wishlist_items': wishlist_items


    })    

def account_view(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)

    if request.method == "POST":

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        addr = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        #  VALIDATION
        if not all([name, phone, addr, city, pincode]):
            return redirect('account')

        Address.objects.create(
            user_id=user_id,
            name=name,
            phone=phone,
            address=addr,
            city=city,
            pincode=pincode
        )

        return redirect('account')

    #fetch after POST (cleaner)
    addresses = Address.objects.filter(user_id=user_id)

    return render(request, 'users/account.html', {
        'addresses': addresses,
        'user':user
    })


def logout_view(request):
    request.session.flush()
    return redirect("login")


from products.models import Product

def user_products(request):

    if 'user_id' not in request.session:
        return redirect('login')
    
    user_id = request.session.get('user_id')

    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

        wishlist_items = Wishlist.objects.filter(user_id=user_id)\
                        .values_list('product_id', flat=True)

    return render(request, 'users/home.html', {
        'products': products
    })

from django.shortcuts import redirect
from .models import Address

def delete_address(request, id):
    if 'user_id' not in request.session:
        return redirect('login')

    address = Address.objects.get(id=id)

    # safety: only delete own address
    if address.user_id == request.session['user_id']:
        address.delete()

    return redirect('account')


def add_to_wishlist(request, product_id):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')

    # avoid duplicate
    if not Wishlist.objects.filter(user_id=user_id, product_id=product_id).exists():
        Wishlist.objects.create(user_id=user_id, product_id=product_id)

    return redirect('user_products')

def view_wishlist(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')

    wishlist = Wishlist.objects.filter(user_id=user_id)

    return render(request, 'users/wishlist.html', {
        'wishlist': wishlist
    })

def remove_from_wishlist(request, product_id):
    user_id = request.session.get('user_id')
    Wishlist.objects.filter(user_id=user_id, product_id=product_id).delete()
    return redirect('wishlist')

from django.http import JsonResponse
from .models import Wishlist

from django.http import JsonResponse
from products.models import Product
from .models import Wishlist

def toggle_wishlist(request, product_id):
    if 'user_id' not in request.session:
        return JsonResponse({"status": "login_required"})

    user_id = request.session.get('user_id')

    item = Wishlist.objects.filter(
        user_id=user_id,
        product_id=product_id
    )

    if item.exists():
        item.delete()
        return JsonResponse({"status": "removed"})
    else:
        Wishlist.objects.create(
            user_id=user_id,
            product_id=product_id
        )
        return JsonResponse({"status": "added"})