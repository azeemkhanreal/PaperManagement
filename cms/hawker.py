from django.shortcuts import render, HttpResponse, redirect
from .models import Customer, Hawker, Invoice
import datetime

def add_hawker(request):
    if request.session.has_key('username'):
        username = request.session['username']

        current_date = datetime.date.today()

        # Insert hawker entries in database
        if request.method == 'POST':
            hawker_name = request.POST["hawker_name"]
            hawker_mobile = request.POST["hawker_mobile"]
            hawker_address = request.POST["hawker_address"]
            hawker_date = datetime.date.today()
            hawker_info = Hawker(hawker_name=hawker_name, hawker_mobile=hawker_mobile,
                                    hawker_address=hawker_address, hawker_date=hawker_date)
            hawker_info.save()
            return redirect('add_hawker')
        else:
            return render(request, 'cms/hawker/add_hawker.html', {'current_date': current_date})
        return render(request,'cms/hawker/add_hawker.html')
    else:
        return redirect('login')

###################
# Hawker Report
###################


def hawker_report(request):
    if request.session.has_key('username'):
        username = request.session['username']

        # filter all customer details
        all_hawker = Hawker.objects.all()

        return render(request, 'cms/hawker/hawker_report.html', {'hawker': all_hawker})
    else:
        return redirect('login')

def hawker_update(request,pk):
   if request.session.has_key('username'):
        username = request.session['username']

        if request.method=='POST':
            hawker_filter = Hawker.objects.get(hawker_id=pk)
            hawker_filter.hawker_name = request.POST["hawker_name"]
            hawker_filter.hawker_mobile = request.POST["hawker_mobile"]
            hawker_filter.hawker_address = request.POST["hawker_address"]
            hawker_filter.save()

            return redirect('hawker_report')

        return redirect('hawker_report')
   else:
        return redirect('login')

# Delete Hawker


def delete_hawker(request, pk):
    if request.session.has_key('username'):
        username = request.session['username']

        hawker_filter = Hawker.objects.get(hawker_id=pk)
        if hawker_filter:
            hawker_filter.delete()
        else:
            return HttpResponseRedirect('cms/hawker_report/')
        return redirect('hawker_report')
    else:
        return redirect('login')
