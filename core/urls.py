from django.urls import path, include

from rest_framework.routers import DefaultRouter

from core.views import (
    dashboard_view, product_list_view, order_list_view, 
    product_detail_view, product_edit_view, product_delete_view,
    order_detail_view, order_edit_view, order_delete_view,
    ProductViewSet, OrderViewSet, FileUploadView,
    create_product_view, create_order_view, create_invoice_view
)


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'file-upload', FileUploadView, basename='file-upload')

urlpatterns = [
    path('', dashboard_view, name='index'),
    path('products/create/', create_product_view, name='create_product'),
    path('orders/create/', create_order_view, name='create_order'),
    path('invoices/create/', create_invoice_view, name='create_invoice'),
    path('products/', product_list_view, name='products'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('products/<int:pk>/edit/', product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', product_delete_view, name='product_delete'),
    path('orders/', order_list_view, name='orders'),
    path('orders/<int:pk>/', order_detail_view, name='order_detail'),
    path('orders/<int:pk>/edit/', order_edit_view, name='order_edit'),
    path('orders/<int:pk>/delete/', order_delete_view, name='order_delete'),
    path('api/', include(router.urls)),
]
