from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from app.models import Purchase_Order, Purchase_Order_Item
from django.contrib.auth.models import User

# Create your views here.

@login_required
def showpo(request):
    polist = Purchase_Order.objects.filter(finance_officer = request.user)
    all_users = User.objects.all()
    context = {
        'title': 'Purchase Order List',
        'year': datetime.now().year,
        'polist' : polist,
        'all_users' : all_users
    }
    context['user'] = request.user
    return render(request,'viewpo/polist.html',context)
    
def viewpoform(request):
    newpurchase_order_id= request.POST['purchase_order_id']
    if(Purchase_Order.objects.filter(purchase_order_id=newpurchase_order_id).exists()):
        pos = Purchase_Order.objects.filter(purchase_order_id=newpurchase_order_id)
        po = pos[0]
        newquotation_id = po.quotation.quotation_id
        poitems = Purchase_Order_Item.objects.filter(purchase_order_id = newpurchase_order_id)

        context = {
                'title': 'Quotation List',
                'year': datetime.now().year,
                'purchase_order_id' : newpurchase_order_id,
                'po' : po,
                'quotation_id': newquotation_id,
                'finance_officer' : request.user.get_username(),
                'total_price': po.total_price,
                'purchase_order_created_date' : po.purchase_order_created_date,
                'delivery_date' : po.delivery_date,
                'purchase_order_status' : po.purchase_order_status,
                'poitems' : poitems,
            }
    else:
        messages.error(request, 'Purchase Order ' + newpurchase_order_id + ' not found!')
        return render(request,'viewpo/error.html')

    return render(request,'viewpo/viewpoform.html',context)
