from django.shortcuts import render, redirect
from django.db.models import Sum
from decimal import *
from .models import Order, Product

getcontext().prec = 2

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def purchase(request):
    if request.method == "POST":
        quantity_from_form = int(request.POST["quantity"])
        price_of_product = float(Product.objects.get(id=request.POST["product_id"]).price)
        total_charge = quantity_from_form * price_of_product
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        return redirect("/checkout")
    return redirect('/')

def checkout(request):
    context = {
        "last_order": Order.objects.last(),
        "num_orders": Order.objects.count(),
        "total_items": Order.objects.all().aggregate(Sum('quantity_ordered'))['quantity_ordered__sum'],
        "grand_total": round(Order.objects.all().aggregate(Sum('total_price'))['total_price__sum'], 2),
    }
    print(context['grand_total'])
    return render(request, "store/checkout.html", context)