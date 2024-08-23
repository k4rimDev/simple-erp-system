from django.contrib import admin

from core.models import (
    Customer, Product, Order, 
    OrderItem, Invoice, Payment
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock')
    search_fields = ('name', 'sku')
    list_filter = ('price', 'stock')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_amount', 'created_at')
    search_fields = ('customer__name', 'status')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'order', 'total_amount', 'created_at', 'due_date')
    search_fields = ('invoice_number', 'order__customer__name')
    list_filter = ('created_at', 'due_date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'payment_date', 'method')
    search_fields = ('invoice__invoice_number',)
    list_filter = ('payment_date', 'method')
