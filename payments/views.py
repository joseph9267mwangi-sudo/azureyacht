from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bookings.models import Booking
from .models import MpesaTransaction
from .utils import initiate_stk_push
import json

def checkout(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = 1  # replace with real pricing logic later

        callback_url="https://tricycle-roamer-monkhood.ngrok-free.dev/payments/callback/"

        transaction = MpesaTransaction.objects.create(
            booking=booking,
            phone_number=phone_number,
            amount=amount,
        )

        response = initiate_stk_push(
            phone_number=phone_number,
            amount=amount,
            callback_url=callback_url,
            account_reference=f"AzureYacht-{booking.id}"
        )

        print("MPESA RESPONSE:",response)
        transaction.checkout_request_id = response.get('CheckoutRequestID')
        transaction.merchant_request_id = response.get('MerchantRequestID')
        transaction.save()

        return render(request, 'payments/waiting.html', {'transaction': transaction})

    return render(request, 'payments/checkout.html', {'booking': booking})


@csrf_exempt
def mpesa_callback(request):
    print("CALLBACK RECIEVED")
    data = json.loads(request.body)
    result = data['Body']['stkCallback']

    checkout_request_id = result.get('CheckoutRequestID')
    result_code = result.get('ResultCode')
    result_desc = result.get('ResultDesc')

    try:
        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
    except MpesaTransaction.DoesNotExist:
        return JsonResponse({'status': 'transaction not found'}, status=404)

    if result_code == 0:
        transaction.status = 'success'
        metadata = result['CallbackMetadata']['Item']
        for item in metadata:
            if item['Name'] == 'MpesaReceiptNumber':
                transaction.mpesa_receipt_number = item['Value']
        transaction.booking.status = 'paid'
        transaction.booking.save()
    else:
        transaction.status = 'failed'

    transaction.result_desc = result_desc
    transaction.save()

    return JsonResponse({'status': 'received'})


