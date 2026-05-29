
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from users.models import Wishlist

from products.models import ProductImage

def add_product(request):

    # ✅ OWNER CHECK (your system)
    if 'owner_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            images = request.FILES.getlist('images')

            for img in images:
                ProductImage.objects.create(
                    product=product,
                    image=img
                )

            return redirect('owner_products')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})

from django.shortcuts import get_object_or_404
from .models import ProductImage

def edit_product(request, product_id):

    # OWNER CHECK
    if 'owner_id' not in request.session:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            # NEW IMAGES
            images = request.FILES.getlist('images')

            if images:

                # remove old images
                ProductImage.objects.filter(
                    product=product
                ).delete()

                # add new images
                for img in images:

                    ProductImage.objects.create(
                        product=product,
                        image=img
                    )

            return redirect('owner_products')

    else:

        form = ProductForm(instance=product)

    context = {

        'form': form,
        'product': product
    }

    return render(
        request,
        'products/edit_product.html',
        context
    )

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

from django.shortcuts import get_object_or_404

def delete_product(request, product_id):

    if 'owner_id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        product.delete()

    return redirect('owner_products')



def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)
    images = []
    for img in product.images.all():
        images.append(img.image.url)
    
    
    user_id = request.session.get('user_id')

    wishlist_items = Wishlist.objects.filter(
        user_id=user_id
    ).values_list('product_id', flat=True)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'wishlist_items': wishlist_items
        
    })

