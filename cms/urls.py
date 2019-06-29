from django.contrib import admin
from django.urls import path
from cms import views, hawker
urlpatterns = [
    path("", views.cms_home, name="cms_home"),
    path('add_customer/',views.add_customer, name = "add_customer"),
    path('customer_update/<int:pk>', views.customer_update, name="customer_update"),
    path('delete_customer/<int:pk>', views.delete_customer, name="delete_customer"),
    path('customer_report/',views.customer_report, name="customer_report"),
    path('collect_amount/<int:pk>', views.collect_amount, name="collect_amount"),
    path('invoice_update/<int:pk>', views.invoice_update, name="invoice_update"),
    path('search_customer/',views.search_customer, name="search_customer"),


# Hawker Routing
    path('add_hawker/', hawker.add_hawker, name="add_hawker"),
    path('delete_hawker/<int:pk>', hawker.delete_hawker, name="delete_hawker"),
    path('hawker_report/', hawker.hawker_report, name="hawker_report"),
    path('hawker_update/<int:pk>', hawker.hawker_update, name="hawker_update"),

]
