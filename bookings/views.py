from django.shortcuts import render, redirect
from .models import Booking
from django.core.mail import send_mail
import os 
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
def send_booking_email(first_name, last_name, email, phone, yacht, guests, date, duration, message,):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email_content = (
        f"Name: {first_name} {last_name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Yacht:{yacht}\n"
        f"Guests: {guests}\n"
        f"Date: {date}\n"
        f"Duration {duration}\n"
        f"Message {message}"
    )
    def send_customer_confirmation_email(first_name, last_name, email, yacht, guests, date, duration, message):
        configuration= sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

        api_insurance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        configuration_content = (
            f"hi {first_name}, \n\n"
            f"Thankyou for booking with Azureyacht! Here are your booking details :\n\n"
            f"yacht: {yacht}\n"
            f"Guests: {guests}\n"
            f"Duration: {duration}\n"
            f"message: {message}\n\n"
            f"we will be in touch shortly to confirm your booking.\n\n"
            f"best regards, \nAzureyacht team" 
        )
        send_smtp_email= sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": email}],
                sender={"email": "joseph9267mwangi@gmail.com","name": "Azureyacht"},
                subject="your Azureyacht Booking confirmation",
                text_content=configuration_content
            )
        api_instance.send_transac_email(send_smtp_email)

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "joseph9267mwangi@gmail.com"}],
            sender={"email": "joseph9267mwangi@gmail.com", "name": "AzureYacht"},
            subject=f"New Booking from {first_name} {last_name}",
            text_content=email_content
        )
        api_instance.send_transac_email(send_smtp_email)

def home(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        yacht = request.POST.get('yacht','')
        guests = request.POST.get('guests','')
        date = request.POST.get('date','')
        duration=request.POST.get('duration','')
        message=request.POST.get('message','')

        Booking.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            yacht=yacht,
            guests=guests,
            date=date,
            duration=duration,
            message=message,
        )
        send_booking_email(first_name, last_name, email, phone, yacht, guests, date, duration, message)
        send_customer_confirmation_email(first_name, last_name, email, yacht, guests, date, duration, message)
        return render(request, 'bookings/success.html')
    
    return render(request, 'bookings/index.html')

def success(request):
    return render(request, 'booking/index.html')