from django.shortcuts import render, HttpResponse, redirect
from .models import Customer, Hawker, Invoice


def send_email(request):
    return render(request, 'cms/communication/send_email.html')
