from django.db import models
from bookings.models import Booking

class MpesaTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('success', 'success'),
        ('failed', 'failed'),

    ]
    booking= models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mpesa_reciept_number = models.CharField(max_length=50, blank=True, null=True)
    result_desc = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking} - {self.status} - {self.amount}"
    
