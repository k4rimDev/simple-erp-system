from celery import shared_task
from core.models import Order, Invoice
import uuid


@shared_task
def generate_invoice(order_id):
    order = Order.objects.get(id=order_id)
    total_amount = sum(item.product.price * item.quantity for item in order.items.all())
    invoice = Invoice.objects.create(
        order=order,
        invoice_number=str(uuid.uuid4()),
        total_amount=total_amount
    )
    return invoice.invoice_number
