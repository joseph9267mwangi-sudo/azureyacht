from django.urls import path
from . import views
urlpatterns = [
    path('checkout/<int:booking_id>/', views.checkout, name='checkout'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
    
]