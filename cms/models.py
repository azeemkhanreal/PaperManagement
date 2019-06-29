from django.db import models
from django.utils import timezone

# Hawker Information
class Hawker(models.Model):
    hawker_id = models.AutoField(db_column='ID', primary_key=True)
    hawker_name = models.CharField(max_length=50, default="")
    hawker_mobile = models.CharField(max_length=40, default="")
    hawker_address = models.CharField(max_length=50, default="")
    hawker_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.hawker_name

# Customer Information
class Customer(models.Model):
    customer_id = models.AutoField(db_column='ID', primary_key=True)
    customer_name = models.CharField(max_length=50, default="")
    customer_mobile = models.CharField(max_length=40, default="")
    customer_email = models.CharField(max_length=40, default="")
    customer_address = models.CharField(max_length=50, default="")
    customer_date = models.DateTimeField(blank=True, null=True)
    hawker = models.ForeignKey(
        Hawker, default=1, verbose_name='hawker', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.customer_name


# Fee

class Invoice(models.Model):
    customer_id = models.ForeignKey(
        Customer, default=1, verbose_name='customer', on_delete=models.CASCADE)
    id = models.AutoField(db_column='ID', primary_key=True)
    i_sr = models.CharField(max_length=40, default="")
    i_date = models.DateTimeField(blank=True, null=True)
    i_month = models.CharField(max_length=40, default="")
    i_amount = models.IntegerField(blank=True, null=True)
    i_status = models.CharField(max_length=40, default="")
    i_paid = models.IntegerField(blank=True, null=True)
    i_description = models.CharField(max_length=40, default="")
    class Meta:
        verbose_name_plural = 'invoice'

    def __str__(self):
        return self.i_sr
