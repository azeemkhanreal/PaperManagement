from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
import datetime
from .models import Customer, Hawker, Invoice
from django.db.models import Q, Sum
import calendar

current_date = datetime.date.today()
# Get Last Month
now = datetime.datetime.now()
last_month = now.month-1 if now.month > 1 else 12
month_name = "January Fabruary March April May June July August September October November December".split()[
    last_month-1]

###################
# CMS Dashboard
###################

def cms_home(request):
    if request.session.has_key('username'):
        username = request.session['username']

        all_customer = Customer.objects.all()

        all_hawker = Hawker.objects.all()

        return render(request, 'cms/dashboard.html', {'all_customer': all_customer, 'all_hawker': all_hawker, 'username': username})
    
    else:
        return redirect('login')

# Add Customer 


def add_customer(request):
    if request.session.has_key('username'):
        username = request.session['username']

        all_hawker = Hawker.objects.all()

        # Insert customer entries in database
        if request.method == 'POST':
            customer_name = request.POST["customer_name"]
            customer_mobile = request.POST["customer_mobile"]
            customer_address = request.POST["customer_address"]
            customer_date = datetime.date.today()
            hawker_name = request.POST['hawker_name']
            hawker= Hawker.objects.get(hawker_name=hawker_name)
            customer_info = Customer(customer_name=customer_name, customer_mobile=customer_mobile,
                                customer_address=customer_address, customer_date=customer_date,hawker = hawker)
            customer_info.save()

        return render(request, 'cms/customer/add_customer.html', {'current_date': current_date, 'all_hawker': all_hawker, 'username': username})
 
    else:
        return redirect('login')


###################
# Customer Report
###################

def customer_report(request):
    if request.session.has_key('username'):
        username = request.session['username']
        # filter all customer details
        all_customer = Customer.objects.all()
        all_hawker = Hawker.objects.all()

        return render(request, 'cms/customer/customer_report.html', {'customers': all_customer, 'all_hawker': all_hawker})
    
    else:
        return redirect('login')




def collect_amount(request,pk):
    if request.session.has_key('username'):
        username = request.session['username']

        customer_filter = Customer.objects.get(customer_id=pk)

        all_invoice = Invoice.objects.all()

        last_invoice = Invoice.objects.all().order_by('i_sr').last()
        if not last_invoice:
            new_invoice_no = 'AU00001'
        else:
            invoice_no = last_invoice.i_sr
            invoice_int = int(invoice_no.split('AU')[-1])
            new_invoice_int = invoice_int+1
            new_invoice_no = 'AU' + '0000' + str(new_invoice_int)

        # Create New Invoice
        if request.method == 'POST':
            invoice_date = request.POST['i_date']
            invoice_sr = new_invoice_no
            invoice_status = request.POST['i_status']
            invoice_month = request.POST['i_month']
            invoice_description = request.POST['i_desc']
            invoice_amount = request.POST['i_total']
            invoice_name = request.POST['customer_name']
            invoice_paid = request.POST['i_paid']
            i_customer = Customer.objects.get(customer_name=invoice_name)
            invoice_info = Invoice(customer_id=i_customer, i_sr=invoice_sr, i_date=invoice_date, i_month=invoice_month, i_amount=invoice_amount,
                                i_description=invoice_description, i_status=invoice_status, i_paid=invoice_paid)
            invoice_info.save()

            return HttpResponseRedirect("")

        return render(request, 'cms/customer/collect_amount.html', {'customer': customer_filter, 'current_date': current_date, 'invoice_no': new_invoice_no, 'all_invoice': all_invoice, 'username': username})

    else:
        return redirect('login')

def invoice_update(request,pk):
    if request.session.has_key('username'):
        username = request.session['username']
        
        if request.method=='POST':
            invoice_filter = Invoice.objects.get(id=pk)
            invoice_filter.i_sr = request.POST['i_sr']
            invoice_filter.i_date = request.POST['i_date']
            invoice_filter.i_month = request.POST['i_month']
            invoice_filter.i_status = request.POST['i_status']
            invoice_filter.i_description = request.POST['i_description']
            invoice_filter.i_amount = request.POST['i_amount']
            invoice_filter.i_paid = request.POST['i_paid']
            c_id = request.POST['customer_id']
            invoice_filter.save()

            return redirect('collect_amount',pk =c_id)

    else:
        return redirect('login')

def customer_update(request, pk):
    if request.session.has_key('username'):
        username = request.session['username']

        if request.method == 'POST':
            customer_filter = Customer.objects.get(customer_id=pk)
            customer_filter.customer_name = request.POST["customer_name"]
            customer_filter.customer_mobile = request.POST["customer_mobile"]
            customer_filter.customer_email = request.POST["customer_email"]
            customer_filter.customer_address = request.POST["customer_address"]
            hawker_name = request.POST['hawker_name']
            hawker = Hawker.objects.get(hawker_name=hawker_name)
            customer_filter.hawker = hawker
            customer_filter.save()

            return redirect('customer_report')

        return redirect('customer_report')
   
    else:
        return redirect('login')

# Delete Customer


def delete_customer(request, pk):
    if request.session.has_key('username'):
        username = request.session['username']

        customer_filter = Customer.objects.get(customer_id=pk)
        if customer_filter:
            customer_filter.delete()
        else:
            return HttpResponseRedirect('cms/customer_report/')
        return redirect('customer_report')

    else:
        return redirect('login')


# Search Customer

###################
# Customer Search
###################

def search_customer(request):
    if request.session.has_key('username'):
        username = request.session['username']

        # if user search records then
        if request.method == 'POST':
            keyword = request.POST['search']
            if keyword:
                all_customer = Customer.objects.filter(
                    Q(customer_name__icontains=keyword) | Q(customer_mobile__icontains=keyword))

                return render(request, 'cms/customer/customer_report.html', {'customers': all_customer, 'username': username})
            else:
                return redirect('customer_report')
        else:
            return redirect('customer_report')

    else:
        return redirect('login')
