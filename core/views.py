from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    Customer, Product, Order, 
    OrderItem, Invoice, Payment
)
from core.serializers import (
    CustomerSerializer, ProductSerializer, 
    OrderSerializer, InvoiceSerializer, 
    PaymentSerializer, OrderItemSerializer
)
from core.tasks import generate_invoice

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        order_id = response.data['id']
        generate_invoice.delay(order_id)
        return Response(response.data, status=status.HTTP_201_CREATED)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
