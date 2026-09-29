from django.contrib import admin

# Register your models here.
from .models import Tour, Reserva

admin.site.register(Tour)
admin.site.register(Reserva)