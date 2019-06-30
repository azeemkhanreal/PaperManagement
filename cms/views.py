from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
import datetime
from .models import Customer, Hawker, Invoice, monthCost
from django.db.models import Q, Sum
import calendar

current_date = datetime.date.today()
# Get Last Month
now = datetime.datetime.now()
last_month = now.month-1 if now.month > 1 else 12
last_month_name = "January February March April May June July August September October November December".split()[
    last_month-1]
all_month_name = "January February March April May June July August September October November December".split()

###################
# CMS Dashboard
###################


def cms_home(request):
    if request.session.has_key('username'):
        username = request.session['username']

        all_customer = Customer.objects.all()

        all_hawker = Hawker.objects.all()

        collect_month_amount = Invoice.objects.filter(
            i_status='Paid', i_month=last_month_name).aggregate(Sum('i_paid'))

        collect_annual_amount = Invoice.objects.filter(
            i_status='Paid').aggregate(Sum('i_paid'))
        print(collect_annual_amount['i_paid__sum'])

        #  Amount Collection Charts  JS

        collection_chart = Invoice.objects.filter(
            i_status='Paid').annotate(Sum('i_paid'))
        for x in collection_chart:
            print(x.i_month)

        # if month cost is not set in database then automatically generate data
        month_cost = monthCost.objects.all()

        if not month_cost:
            for x in all_month_name:
                month_cost_info = monthCost(month=x, amount=0)
                month_cost_info.save()

        return render(request, 'cms/dashboard.html', {'all_customer': all_customer, 'all_hawker': all_hawker, 'collection_chart': collection_chart, 'collect_month_amount': collect_month_amount, 'collect_annual_amount': collect_annual_amount, 'username': username})

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
            hawker = Hawker.objects.get(hawker_name=hawker_name)
            customer_info = Customer(customer_name=customer_name, customer_mobile=customer_mobile,
                                     customer_address=customer_address, customer_date=customer_date, hawker=hawker)
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


def collect_amount(request, pk):
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
            month_amount = monthCost.objects.get(
                month=invoice_month)  # get monthcost
            invoice_amount = month_amount.amount  # month_cost = invoice month amount
            invoice_description = request.POST['i_desc']
            invoice_name = request.POST['customer_name']
            invoice_paid = request.POST['i_paid']
            i_customer = Customer.objects.get(customer_name=invoice_name)
            invoice_info = Invoice(customer_id=i_customer, i_sr=invoice_sr, i_date=invoice_date, i_month=invoice_month, i_amount=invoice_amount,
                                   i_description=invoice_description, i_status=invoice_status, i_paid=invoice_paid)
            invoice_info.save()

            return HttpResponseRedirect("")

        # Monthly Cost
        month_cost = monthCost.objects.all()

        return render(request, 'cms/customer/collect_amount.html', {'customer': customer_filter, 'current_date': current_date, 'invoice_no': new_invoice_no, 'all_invoice': all_invoice, 'username': username, 'month_cost': month_cost})

    else:
        return redirect('login')


def delete_invoice(request, pk):
    if request.session.has_key('username'):
        username = request.session['username']

        invoice_filter = Invoice.objects.get(id=pk)
        if invoice_filter:
            invoice_filter.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login')


def invoice_update(request, pk):
    if request.session.has_key('username'):
        username = request.session['username']

        if request.method == 'POST':
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

            return redirect('collect_amount', pk=c_id)

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


def manage_month_cost(request):
    if request.session.has_key('username'):
        username = request.session['username']

        month_cost = monthCost.objects.all()

        # Update monthly_cost in database
        if request.method == 'POST':
            for x in month_cost:
                if x.month == 'January':
                    x.amount = request.POST['January']
                    x.save()
                if x.month == 'February':
                    x.amount = request.POST['February']
                    x.save()
                if x.month == 'March':
                    x.amount = request.POST['March']
                    x.save()
                if x.month == 'April':
                    x.amount = request.POST['April']
                    x.save()
                if x.month == 'May':
                    x.amount = request.POST['May']
                    x.save()
                if x.month == 'June':
                    x.amount = request.POST['June']
                    x.save()
                if x.month == 'July':
                    x.amount = request.POST['July']
                    x.save()
                if x.month == 'August':
                    x.amount = request.POST['August']
                    x.save()
                if x.month == 'September':
                    x.amount = request.POST['September']
                    x.save()
                if x.month == 'October':
                    x.amount = request.POST['October']
                    x.save()
                if x.month == 'November':
                    x.amount = request.POST['November']
                    x.save()
                if x.month == 'December':
                    x.amount = request.POST['December']
                    x.save()
                message = 'Data Update'
        return render(request, 'cms/manage_month_cost.html', {'month_cost': month_cost})

    else:
        return redirect('login')
