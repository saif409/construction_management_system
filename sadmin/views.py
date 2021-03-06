from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from supply_management.models import Stock, SiteManageger, Author, Labour, Client, Supplier, Supply
from construction_management.utils import current_year,current_month,today

# Create your views here.


def testview(request):
    return HttpResponse(request, "this is test")


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            user = request.POST.get('user', )
            password = request.POST.get('pass', )
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch!')
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    day = today()
    month=current_month()
    year= current_year()

    total_employee = Author.objects.all().count()
    total_labour = Labour.objects.all().count()
    total_client = Client.objects.all().count()
    stock_obj = Stock.objects.all()
    total_quantity = stock_obj.aggregate(Sum('quantity'))['quantity__sum']

    site_obj = SiteManageger.objects.filter(is_approve=1)
    total_quantity_site = site_obj.aggregate(Sum('quantity'))['quantity__sum']


    daily_stock = Stock.objects.all().filter(created_date=day).aggregate(Sum('quantity'))['quantity__sum']
    if daily_stock is None:
        daily_stock = 0

    monthly_stock = Stock.objects.all().filter(created_date__month=month).aggregate(Sum('quantity'))['quantity__sum']
    if monthly_stock is None:
        monthly_stock = 0

    yearly_stock = Stock.objects.all().filter(created_date__year=year).aggregate(Sum('quantity'))['quantity__sum']
    if yearly_stock is None:
        yearly_stock = 0


    if total_quantity_site is None:
        total_quantity_site = 0
    if total_quantity is None:
        total_quantity = 0
    total = total_quantity - total_quantity_site
    client_obj = Client.objects.all()[::-1]
    suply_obj = Supply.objects.all()[::-1]

    context={
        'daily_stock':daily_stock,
        'monthly_stock':monthly_stock,
        'yearly_stock':yearly_stock,
        'day':today,
        'month' : current_month(),
        'year':  current_year(),
        "obj":stock_obj,
        "suply_obj": suply_obj,
        "total_employee":total_employee,
        "total_labour":total_labour,
        "total_client":total_client,
        "isact_home": "active",
        'stock':total_quantity,
        'total_quantity':total_quantity_site,
        "total":total,
        "client_obj":client_obj
    }
    return render(request, "admin_home.html", context)
