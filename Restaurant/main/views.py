"""
 this is only views.py page which is used to handle all page
"""
import re

from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib  import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import Momo

# Create your views here.
date=datetime.now()

@login_required(login_url='log_in')
def index(request):
    buf=Momo.objects.filter(category='buf')
    chicken=Momo.objects.filter(category='chicken')
    veg=Momo.objects.filter(category='veg')


    return render(request,'main/index.html',{'date':date,'buf':buf,"chicken":chicken,'veg':veg})

@login_required(login_url='log_in')
def about(request):
    return render(request,'main/about.html')
def contact(request):
    return render(request,'main/contact.html')
def menu(request):
    return render(request,'main/menu.html')
def service(request):
    return render(request,'main/services.html')

'''
====================================================================
====================================================================
                           Authentication Part
====================================================================
====================================================================

'''
def register(request): 
    ''' it used to take information from user''' 
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']       
        if password==password1:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,'your username is already exists!!!')
                    return redirect('register')
                
                elif not re.search(r'[A-Z]',password):
                    messages.error(request,'your password should contain at least one upper letter!!!')
                    return redirect('register')
                elif not re.search(r'\d',password):
                    messages.error(request,'your password should contain at least one digit!!!')
                    return redirect('register')
                
                elif not re.search(r"[!@#$%^&*()<>]",password):
                    messages.error(request,'your password must contain at least one symbol')
                    return redirect("register")
                   
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'your email is already exists!!!')
                    return redirect('register')    
                else:
            
                    User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    return redirect('log_in')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')                 
        else:
            messages.error(request,'password doesnot match!!!')
            return redirect('register')         
    return render(request,'auth/register.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST['username'] #sujan710
        password=request.POST['password'] #ram
        remember_me=request.POST.get('remember_me')  
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register ")
            return redirect('log_in') 
        user=authenticate(username=username,password=password) #None
        if user is not None:
            if remember_me:
                request.session.set_expiry(120000000)
            else:
                request.session.set_expiry(0)
            login(request,user)           
            return redirect('index')
        else:
            messages.error(request,'Invalid Password')
            return redirect("log_in")
    return render(request,'auth/login.html')

def log_out(request):
    ''' this is only for logout page'''
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    '''only for check'''
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,'auth/change_password.html',{'form':form})
