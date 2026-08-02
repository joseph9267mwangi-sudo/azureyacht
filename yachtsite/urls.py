from django.contrib import admin
from django.urls import path, include, re_path #combined re_path here
from django.conf import settings
from django.views.static import serve
from bookings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 1. update this line to point to your new form handler view
    path('',views.home, name='home'),
    path('success/', views.success,name='success'),
    path('payments/', include('payments.urls')),
    #2. FORCE STATIC FILES TO SERVE EVEN WHEN THE DEBUG=FALSE
    re_path(r'^static/(?P<path>.*)',serve, {'document_root': settings.STATIC_ROOT}),
]