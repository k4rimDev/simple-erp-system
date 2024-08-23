from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from rest_framework import viewsets, status

from core.models import (
    Customer, Product, Order, 
    OrderItem, Invoice, Payment
)
from core.serializers import (
    CustomerSerializer, ProductSerializer, 
    OrderSerializer, InvoiceSerializer, PaymentSerializer
)
from core.forms import ProductForm, OrderForm, InvoiceForm


def dashboard_view(request):
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_invoices = Invoice.objects.count()
    return render(request, 'index.html', {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_invoices': total_invoices,
    })

def create_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

def create_order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            order.calculate_total()
            return redirect('orders')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

def create_invoice_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = InvoiceForm()
    return render(request, 'create_invoice.html', {'form': form})

def product_list_view(request):
    products = Product.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
    return render(request, 'products.html', {'products': products, 'search_query': search_query})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_edit.html', {'form': form, 'product': product})

def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'product_delete_confirm.html', {'product': product})

def order_list_view(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})

def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})

def order_edit_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'order': order})

def order_delete_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orders')
    return render(request, 'order_delete_confirm.html', {'order': order})

# API Views

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class FileUploadView(viewsets.ViewSet):
    def create(self, request):
        file = request.FILES.get('file')
        order_id = request.data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        order.document = file
        order.save()
        return JsonResponse({'message': 'File uploaded successfully'}, status=status.HTTP_200_OK)
