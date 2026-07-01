from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'yacht', 'date', 'status']
    list_flter = ['status']
    actions = ['approve_bookings']

    def approve_bookings(self, request,queryset):
        queryset.update(status='approved')
    approve_bookings.short_description = 'Approve selected bookings'