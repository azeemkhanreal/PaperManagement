# Generated by Django 2.2.2 on 2019-06-26 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_invoice_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='i_description',
            field=models.CharField(default='', max_length=40),
        ),
    ]
