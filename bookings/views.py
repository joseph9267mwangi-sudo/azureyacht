from django.shortcuts import render, redirect
from .models import Booking
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from datetime import datetime
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException



def send_booking_email(first_name, last_name, email, phone, yacht, guests, date, duration, message):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # Email to the owner with booking details
    email_content = (
        f"Name: {first_name} {last_name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Yacht: {yacht}\n"
        f"Guests: {guests}\n"
        f"Date: {date}\n"
        f"Duration: {duration}\n"
        f"Message: {message}"
    )
    owner_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": "joseph9267mwangi@gmail.com"}],
        sender={"email": "joseph9267mwangi@gmail.com", "name": "Azureyacht"},
        subject=f"New Booking from {first_name} {last_name}",
        text_content=email_content
    )
    api_instance.send_transac_email(owner_email)

    # Confirmation email to the customer
    customer_content = (
        f"Hi {first_name},\n\n"
        f"Thank you for booking with Azureyacht! Here are your booking details:\n\n"
        f"Yacht: {yacht}\n"
        f"Guests: {guests}\n"
        f"Duration: {duration}\n"
        f"Message: {message}\n\n"
        f"We will be in touch shortly to confirm your booking.\n\n"
        f"Best regards, \nAzureyacht team"
    )
    customer_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={"email": "joseph9267mwangi@gmail.com", "name": "Azureyacht"},
        subject="Your Azureyacht Booking Confirmation",
        text_content=customer_content
    )
    api_instance.send_transac_email(customer_email)


def home(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        yacht = request.POST.get('yacht', '')
        guests = request.POST.get('guests', '')
        date = request.POST.get('date', '')
        duration = request.POST.get('duration', '')
        message = request.POST.get('message', '')

        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not email:
            errors.append("Email is required.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Please enter a vailid email address.")
        if not phone:
            errors.append("Phone number is required")
        if not yacht:
            errors.append("Please select yacht.")
        if not guests:
            errors.append("number of guests is required")
        else:
            try:
                guests_int = int(guests)
                if guests_int <= 0:
                    errors.append("number of guests must be at least one")
            except ValueError : 
                errors.append("number of guests must be a valid number")
        if not date:
            errors.append("Booking date is required")
        else:
            try:
                 booking_date = datetime.strptime(date, '%Y-%m-%d').date()
                 if booking_date < timezone.now().date():
                      errors.append("Booking date cannot be in the past.")
            except ValueError:
                errors.append("please enter a valid date")
        if errors:
            return render(request, 'bookings/index.html', {'errors': errors})



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
        return render(request, 'bookings/success.html')

    return render(request, 'bookings/index.html')


def success(request):
    return render(request, 'bookings/index.html')