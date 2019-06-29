from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method=='POST':
        # check password confirm equal
        if request.POST['password'] == request.POST['c_password']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'User is alredy exist'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],request.POST['password'])
                auth.login(request,user)
                return redirect('login')

        else:
            return render(request,'accounts/signup.html',{'error':'Password does not match'})  
    else:
        return render(request,'accounts/signup.html')

def login(request):
    if request.method=='POST':
        user = auth.authenticate(username = request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request, user)
            # session create
            request.session['username']=user.first_name
            return redirect('cms_home')
        else:
            return render(request, 'accounts/login.html',{'error':'username or password is incorrect'})
    return render(request, 'accounts/login.html')


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('login')
