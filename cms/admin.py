from django.contrib import admin
from django.contrib import admin
from .models import Customer, Hawker, Invoice, monthCost

# Register your models here.
admin.site.register(Customer)
admin.site.register(Hawker)
admin.site.register(Invoice)
admin.site.register(monthCost)
