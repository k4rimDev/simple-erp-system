from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import (
    CustomerViewSet, ProductViewSet, 
    OrderViewSet, InvoiceViewSet, PaymentViewSet
)


router = DefaultRouter()

router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
