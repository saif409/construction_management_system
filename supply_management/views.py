from django.db.models import Sum
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.base import View

from .models import Supply, Supplier, Stock,Material


# Create your views here.



def supply_add(request):
    obj = Supplier.objects.all()
    material = Material.objects.all()
    context={
        "obj":obj,
        "material":material,
        "isact_supply":"active",
    }
    if request.method =="POST":
        supplier_company_name = request.POST.get("supplier_company_name")
        supplier_company_obj = Supplier.objects.get(name=supplier_company_name)
        material_obj = request.POST.get("material")
        material = Material.objects.get(material_name=material_obj)
        lot_no = request.POST.get("lot_no")
        quantity = request.POST.get("quantity")
        unit_price = request.POST.get("unit_price")
        obj = Supply(supplier_company_name=supplier_company_obj,lot_no=lot_no,quantity=quantity,unit_price=unit_price,material=material)
        obj.save()
        messages.success(request, "Successfully Added To List")
        return redirect('list')
    return render(request, "supply_management/supply_add.html", context)


def supply_list(request):
    obj = Supply.objects.all()
    context={
        "obj":obj,
        "isact_supply": "active",
    }
    return render(request, "supply_management/supply_list.html", context)


def supply_view(request, id):
    obj = get_object_or_404(Supply, id=id)
    context={
        "obj":obj,
        "isact_supply": "active",
    }
    return render(request, "supply_management/supply_view.html", context)


def supply_update(request, id):
    supplier_obj = Supplier.objects.all()
    obj = get_object_or_404(Supply, id=id)
    context={
        "obj":obj,
        "supplier_obj":supplier_obj,
        "isact_supply": "active",
    }
    if request.method == "POST":
        supplier_company = request.POST.get("supplier_company_name")
        get_supplier = Supplier.objects.get(name=supplier_company)
        obj.supplier_company_name = get_supplier
        obj.lot_no = request.POST.get("lot_no")
        obj.quantity = request.POST.get("quantity")
        obj.unit_price = request.POST.get("unit_price")
        obj.save()
        messages.success(request, "Supply Update Successfully")
        return redirect('list')
    return render(request, "supply_management/supply_update.html", context)
#
#
def supply_remove(request, id):
    obj = get_object_or_404(Supply, id=id)
    obj.delete()
    messages.success(request, "Supply Delete Successfully")
    return redirect('list')


def add_supplier(request):
    sup_obj = Supplier.objects.all()[::-1]
    context={
        "supplier":sup_obj,
        "isact_supplier": "active",
    }
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        comments = request.POST.get("comments")
        obj = Supplier(name=name,email=email,phone=phone,address=address,comments=comments)
        obj.save()
        messages.success(request, "supplier Added Successfully ")
        return redirect('add_supplier')
    return render(request, "supply_management/add_new_supplier.html", context)


def update_supplier(request, id):
    supplier_obj = get_object_or_404(Supplier, id=id)
    context={
        "supplier":supplier_obj
    }
    if request.method == "POST":
        supplier_obj.name = request.POST.get("name")
        supplier_obj.email = request.POST.get("email")
        supplier_obj.phone = request.POST.get("phone")
        supplier_obj.address = request.POST.get("address")
        supplier_obj.comments = request.POST.get("comments")
        supplier_obj.save()
        messages.success(request, "Supplier Update Successfully")
        return redirect('add_supplier')
    return render(request, "supply_management/supplier_update.html", context)


def remove_supplier(request, id):
    obj = get_object_or_404(Supplier, id=id)
    obj.delete()
    messages.success(request, "Supplier Removed Successfully")
    return redirect('add_supplier')

# def stock_list(request):
#     obj = Stock.objects.all()[::-1]
#     stock_obj = Stock.objects.all()
#     total_quantity = stock_obj.aggregate(Sum('quantity'))['quantity__sum']
#
#     site_obj = SiteManageger.objects.filter(is_approve=True)
#     total_quantity_site = site_obj.aggregate(Sum('quantity'))['quantity__sum']
#     if total_quantity_site is None :
#         total_quantity_site = 0
#     elif total_quantity is None:
#         total_quantity =0
#     total =int(total_quantity)-int(total_quantity_site)
#
#     context={
#         "obj":obj,
#         "total":int(total),
#         "total_quantity":int(total_quantity),
#         "total_quantity_site":total_quantity_site,
#         "isact_stock": "active",
#     }
#     return render(request, "stock/stock_list.html", context)
#
#
# def add_new_stock(request):
#     obj = Supplier.objects.all()
#     context={
#         "obj":obj,
#         "isact_stock": "active",
#     }
#     if request.method == "POST":
#         supplier_obj = request.POST.get("supplier")
#         supplier = Supplier.objects.get(name=supplier_obj)
#         category = request.POST.get("category")
#         material = request.POST.get("material")
#         quantity = request.POST.get("quantity")
#         stock_obj = Stock(supplier=supplier,category=category,material=material,quantity=quantity,update_by=request.user)
#         stock_obj.save()
#         return redirect('stock_list')
#     return render(request, "stock/add_new_stock.html", context)
#
#
# def site_manager_request_list(request, filter):
#     obj = None
#     if filter == 'None':
#         obj = SiteManageger.objects.all()[::-1]
#     elif filter == 'Approved':
#         obj = SiteManageger.objects.all().filter(is_approve=True)[::-1]
#     elif filter == 'Pending':
#         obj = SiteManageger.objects.all().filter(is_approve=False)[::-1]
#
#     site_obj = SiteManageger.objects.filter(is_approve=True)
#     total_quantity = site_obj.aggregate(Sum('quantity'))['quantity__sum']
#     context = {
#         "obj":obj,
#         'total_required_quantity': total_quantity,
#         "isact_site_manager": "active",
#     }
#     return render(request, "stock/site_manager_request_list.html", context)
#
#
# def site_manager_request(request):
#     if request.method == "POST":
#         category = request.POST.get("category")
#         material = request.POST.get("material")
#         quantity = request.POST.get("quantity")
#         manager_obj = SiteManageger(category=category, material=material, quantity=quantity, site_manager=request.user)
#         manager_obj.save()
#         messages.success(request, "Your Request Send to our Admin, Please Wait for his approval")
#         return redirect('site_manager_request_list', filter='None')
#     context={
#         "isact_site_manager": "active",
#     }
#     return render(request, "stock/site_manager_request.html", context)
#
#
# def site_manager_request_delete(request, id):
#     obj = get_object_or_404(SiteManageger, id=id)
#     obj.delete()
#     messages.success(request, "Successfully Remove")
#     return redirect('site_manager_request_list', filter='None')