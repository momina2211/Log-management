from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Log
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    logs = Log.objects.all().order_by('-timestamp')
    return render(request, 'products/product_list.html', {'products': products, 'logs': logs})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            Log.objects.create(action=f"New product is created Id {product.id} - name {product.name}")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            old_name = product.name
            product = form.save()
            Log.objects.create(action=f"Updated product Id {product.id} - old name {old_name} new name {product.name}")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        Log.objects.create(action=f"Deleted product Id {product.id} - name {product.name}")
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
