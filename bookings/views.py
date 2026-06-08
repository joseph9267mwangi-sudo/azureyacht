from django.shortcuts import render, redirect
from .models import Booking

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
        return redirect('success')
    return render(request,'bookings/index.html')

def success(request):
    return render(request, 'bookings/success.html')
        