from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render

from app.models import Purchase_Requisition, Purchase_Requisition_Item


# Create your views here.
def viewprlist(request):
    prlist = Purchase_Requisition.objects.filter(customer=request.user)
    context = {'prlist': prlist}
    return render(request, 'viewpr/viewprlist.html', context)


def viewpr(request):
    pr_id = request.POST['pr_id']

    if Purchase_Requisition.objects.filter(purchase_requisition_id=pr_id).exists():
        pr = Purchase_Requisition.objects.filter(purchase_requisition_id=pr_id)
        p = pr[0]
        cust_id = Purchase_Requisition.objects.values_list('customer', flat=True).get(purchase_requisition_id=pr_id)
        cust = User.objects.get(id=cust_id)
        pritems = Purchase_Requisition_Item.objects.filter(purchase_requisition_id=pr_id)
        pritems_length = pritems.__len__
        if request.user.id != cust.id:
            messages.error(request, "This Purchase Requisition is not your creation.")
            prlist = Purchase_Requisition.objects.filter(customer=request.user)
            context = {'prlist': prlist}
            return render(request, 'viewpr/viewprlist.html', context)

    else:
        messages.error(request, "Purchase Requisition does not exists")
        prlist = Purchase_Requisition.objects.filter(customer=request.user)
        context = {'prlist': prlist}
        return render(request, 'viewpr/viewprlist.html', context)

    context = {'purchase_requisition_id': pr_id,
               'submitted_date': p.submitted_date,
               'purchase_requisition_status': p.purchase_requisition_status,
               'cust': cust,
               'pritems': pritems,
               'pritems_length': pritems_length, 
               'email': cust.email,
               }
    return render(request, 'viewpr/viewpr.html', context)
