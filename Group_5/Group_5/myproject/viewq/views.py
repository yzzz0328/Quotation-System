from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from app.models import Quotation, Quotation_Item
from django.contrib.auth.models import User

# Create your views here.

@login_required
def showq(request):
    qlist = Quotation.objects.filter(salesman = request.user)
    all_users = User.objects.all()
    context = {
        'title': 'Quotation List',
        'year': datetime.now().year,
        'qlist' : qlist,
        'all_users' : all_users
    }
    context['user'] = request.user
    return render(request,'viewq/qlist.html',context)
    
def viewqform(request):
    newquotation_id= request.POST['quotation_id']
    if(Quotation.objects.filter(quotation_id=newquotation_id).exists()):
        qs = Quotation.objects.filter(quotation_id=newquotation_id)
        q = qs[0]
        newpurchase_requisition_id = q.purchase_requisition.purchase_requisition_id
        cust_ID = Quotation.objects.values_list('customer', flat=True).get(quotation_id = newquotation_id)
        cust = User.objects.get(id = cust_ID)
        qritems = Quotation_Item.objects.filter(quotation_id = newquotation_id)
        if(q.salesman.get_username() == request.user.get_username()): 

            context = {
                'title': 'Quotation List',
                'year': datetime.now().year,
                'quotation_id' : newquotation_id,
                'q' : q,
                'purchase_requisition_id': newpurchase_requisition_id,
                'customer_username' : cust.get_username(),
                'salesman' : request.user.get_username(),
                'quotation_total_price': q.quotation_total_price,
                'created_date' : q.quotation_created_date,
                'quotation_expiry_date' : q.quotation_expiry_date,
                'qitems' : qritems,
            }
        else:
            messages.error(request, 'Quotation ' + newquotation_id + ' is not your creation!')
            return render(request,'viewq/error.html')
    else:
        messages.error(request, 'Quotation ' + newquotation_id + ' not found!')
        return render(request,'viewq/error.html')

    return render(request,'viewq/viewqform.html',context)

