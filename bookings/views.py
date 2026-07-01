from django.shortcuts import render, redirect
from .models import Booking
from django.core.mail import send_mail

def home(request):
    if request.method == 'POST':
        Booking.objects.create(
        first_name=request.POST.get('first_name',''),
        last_name=request.POST.get('last_name',''),
        email=request.POST.get('email',''),
        phone=request.POST.get('phone',''),
        yacht=request.POST.get('yacht',''),
        guests=request.POST.get('guests',''),
        date=request.POST.get('date',''),
        duration=request.POST.get('duration',''),
        message=request.POST.get('message',''),

        )
        return render(request,'bookings/success.html')
    return render(request,'bookings/index.html')
def success(request):
    return render(request,'bookings/index.html')

def submit_booking(request):
    if request.method == 'POST':
        # 1. Capture the data from the html from using request.POST.get('name_attribute)
        first_name = request.POST.get('first_name')
        last_name = request.POST. get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        yacht = request.POST.get('yacht')
        guests = request.POST.get('guests')
        date = request.POST.get('date')
        duration = request.POST.get('duration')
        message = request.POST.get('message','')
        #2. save it directly into the database using your model fields
        booking_entry = Booking.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            yacht=yacht,
            guests=guests,
            date=date,
            duration=duration,
            message=message
        )

        send_mail(
            subject=f'New Booking from {'first_name'} {'last_name'}',
            message=f'Name: {'first_name'}  {'last_name'}\nEmail: {'email'}\nPhone: {'phone'}\nYacht: {'yacht'}\n {'guests'}\nDate: {'date'}\nDuration: {'duration'}\nMessage',
            from_email='joseph9267@gmail.com',
            recipient_list=['joseph9267@gmail.com'],
            fail_silently=False,
        )

            # 3. Direct them to your success screen(the"Boking confirmed"page
        return render(request, 'bookings/success.html')
        
        