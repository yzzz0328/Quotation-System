from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from app.models import Quotation, Quotation_Item


# Create your views here.
@login_required
def viewcqlist(request):
    cqlist = Quotation.objects.filter(customer=request.user)
    context = {'cqlist': cqlist}
    return render(request, 'viewcq/viewcqlist.html', context)


def viewcq(request):
    quotation_id = request.POST['quotation_id']
    if Quotation.objects.filter(quotation_id=quotation_id).exists():
        qs = Quotation.objects.filter(quotation_id=quotation_id)
        q = qs[0]
        purchase_requisition_id = q.purchase_requisition.purchase_requisition_id
        cust_id = Quotation.objects.values_list('customer', flat=True).get(quotation_id=quotation_id)
        cust = User.objects.get(id=cust_id)
        qitems = Quotation_Item.objects.filter(quotation_id=quotation_id)

        if request.user.id != cust.id:
            messages.error(request, "You cannot view this Quotation")
            cqlist = Quotation.objects.filter(customer=request.user)
            context = {'cqlist': cqlist}
            return render(request, 'viewcq/viewcqlist.html', context)
    else:
        messages.error(request, "Quotation does not exists")
        cqlist = Quotation.objects.filter(customer=request.user)
        context = {'cqlist': cqlist}
        return render(request, 'viewcq/viewcqlist.html', context)

    context = {'quotation_id': quotation_id,
               'salesman_id': q.salesman,
               'created_date': q.quotation_created_date,
               'expiry_date': q.quotation_expiry_date,
               'purchase_requisition_id': purchase_requisition_id,
               'quotation_total_price': q.quotation_total_price,
               'qitems': qitems,
               'email' : cust.email,
               }
    return render(request, 'viewcq/viewcq.html', context)
