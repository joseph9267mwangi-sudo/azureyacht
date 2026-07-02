from django.shortcuts import render, redirect
from .models import Booking
from django.core.mail import send_mail

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
        send_mail(
            subject=f'New Booking from {first_name} {last_name}',
            message=f'Name:' + first_name + '' + last_name + '\nEmail: ' + email + '\nPhone: ' + phone + '\nYacht: ' + yacht + '\nGuests:' + guests + '\nDate' + date + '\nDuration:' + duration +'\nMessage: ' + message, 
            from_email='joseph9267mwangi@gmail.com',
            recipient_list=['joseph9267mwangi@gmail.com'],
            fail_silently=False
        )
        return render(request, 'bookings/success.html')
    return render(request, 'bookings/index.html')

def success(request):
    return render(request, 'booking/index.html')