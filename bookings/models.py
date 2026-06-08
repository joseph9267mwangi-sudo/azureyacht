from django.db import models 
class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    yacht = models.CharField(max_length=100)
    guests = models.CharField(max_length=10)
    date = models.CharField(max_length=50)
    duration=models.CharField(max_length=50)
    message = models.TextField(blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
