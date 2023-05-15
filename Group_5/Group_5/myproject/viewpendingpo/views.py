from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from app.models import Purchase_Order, Purchase_Order_Item, Item, Quotation
from django.contrib.auth.models import User
import numpy as np
# Create your views here.

@login_required
def viewpendingpo(request):
    polist = Purchase_Order.objects.filter(purchase_order_status = "Pending").values()
    context = {
        'title': 'Purchase Requisition List',
        'year': datetime.now().year,
        'polist' : polist,
    }
    context['user'] = request.user
    return render(request,'viewpendingpo/viewpendingpolist.html',context)
    
def showpendingpo(request):
    newpurchase_order_id = request.POST['purchase_order_id']    
    if (Purchase_Order.objects.filter(purchase_order_status = "Pending", purchase_order_id = newpurchase_order_id).exists()):
        po = Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('purchase_order_id', 'quotation_id', 'finance_officer_id', 'purchase_order_created_date', 'delivery_date')
        po_id = list(Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('purchase_order_id', flat = True))[0]
        q_id = list(Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('quotation', flat = True))[0]
        fo_id_po = list(Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('finance_officer_id', flat = True))[0]
        fo_id = list(User.objects.filter(id = fo_id_po).values_list('username', flat=True))[0]
        cust_ID = list(Quotation.objects.values_list('customer_id', flat=True).filter(quotation_id = q_id))[0]
        cust_userID = list(User.objects.filter(id = cust_ID).values_list('username', flat=True))[0]
        cust_first_name = list(User.objects.filter(id = cust_ID).values_list('first_name', flat=True))[0]
        cust_last_name = list(User.objects.filter(id = cust_ID).values_list('last_name', flat=True))[0]
        cust_fullname = str(cust_first_name) + " " + str(cust_last_name)
        poitems = Purchase_Order_Item.objects.filter(purchase_order_id = newpurchase_order_id).values_list('item_id', 'item_quantity_PO', 'item_unit_price', 'item_total_price')
        poitems_id = Purchase_Order_Item.objects.filter(purchase_order_id = newpurchase_order_id).values_list('item_id', flat = True)
        items_name = Item.objects.filter(item_id__in = poitems_id).values_list('item_id', 'item_name')
        np_items_name = np.array(list(items_name))
        np_poitems_id = np.array(list(poitems))
        
        item_list = []
        for i in range(len(np_poitems_id)):
            for j in range(len(np_items_name)):
                if (np_poitems_id.T[0][i] == np_items_name.T[0][j]):
                    item_list.append([np_poitems_id.T[0][i], np_items_name.T[1][j], np_poitems_id.T[1][i], np_poitems_id.T[2][i], np_poitems_id.T[3][i]])
        print(item_list)
    else:
        messages.error(request, 'Purchase Order ' + newpurchase_order_id + ' not found!')
        newpurchase_order_id = ''
        return render(request,'viewpendingpo/error.html')
    context = {
        'title': 'Purchase Order Reviewing',
        'year': datetime.now().year,
        'purchase_order_id': newpurchase_order_id,
        'po' : po,
        'po_id' : po_id,
        'item_list': item_list,
        'fo_id' : fo_id,
        'q_id' : q_id,
        'cust_userID' : cust_userID,
        'cust_fullname' : cust_fullname,
    }
    return render(request,'viewpendingpo/viewpendingpo.html',context)

def showpoconfirmation(request):
    newpurchase_order_id = request.POST['purchase_order_id']
    newstatus = request.POST['status']
            
    if (Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).exists()):
        po = Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('purchase_order_id', 'quotation_id', 'finance_officer_id', 'purchase_order_created_date', 'delivery_date')
        po_id = list(Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('purchase_order_id', flat = True))[0]
        q_id = list(Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('quotation', flat = True))[0]
        fo_id_po = list(Purchase_Order.objects.filter(purchase_order_id = newpurchase_order_id).values_list('finance_officer_id', flat = True))[0]
        fo_id = list(User.objects.filter(id = fo_id_po).values_list('username', flat=True))[0]
        cust_ID = list(Quotation.objects.values_list('customer_id', flat=True).filter(quotation_id = q_id))[0]
        cust_userID = list(User.objects.filter(id = cust_ID).values_list('username', flat=True))[0]
        cust_first_name = list(User.objects.filter(id = cust_ID).values_list('first_name', flat=True))[0]
        cust_last_name = list(User.objects.filter(id = cust_ID).values_list('last_name', flat=True))[0]
        cust_fullname = str(cust_first_name) + " " + str(cust_last_name)
        poitems = Purchase_Order_Item.objects.filter(purchase_order_id = newpurchase_order_id).values_list('item_id', 'item_quantity_PO', 'item_unit_price', 'item_total_price')
        poitems_id = Purchase_Order_Item.objects.filter(purchase_order_id = newpurchase_order_id).values_list('item_id', flat = True)
        items_name = Item.objects.filter(item_id__in = poitems_id).values_list('item_id', 'item_name')
        np_items_name = np.array(list(items_name))
        np_poitems_id = np.array(list(poitems))
        
        item_list = []
        for i in range(len(np_poitems_id)):
            for j in range(len(np_items_name)):
                if (np_poitems_id.T[0][i] == np_items_name.T[0][j]):
                    item_list.append([np_poitems_id.T[0][i], np_items_name.T[1][j], np_poitems_id.T[1][i], np_poitems_id.T[2][i], np_poitems_id.T[3][i]])
    else:    
        messages.error(request, 'Purchase Order ' + newpurchase_order_id + ' not found!')
        newpurchase_order_id = ''
        return render(request,'viewpendingpo/error.html')
    
    if newstatus == "Approved":
        pos = Purchase_Order.objects.filter(purchase_order_id=newpurchase_order_id)
        newpo = pos[0]
        newpo.purchase_order_status = "Approved"
        status = "Approved"
        newpo.save()
    elif newstatus == "Rejected":
        pos = Purchase_Order.objects.filter(purchase_order_id=newpurchase_order_id)
        newpo = pos[0]
        newpo.purchase_order_status = "Rejected"
        status = "Rejected"
        newpo.save()
    else:
        messages.error(request, 'Invalid Option')
        newpurchase_order_id = ''
        return render(request,'viewpendingpo/error.html')
        
    context = {
        'title': 'Purchase Order Status Update',
        'year': datetime.now().year,
        'purchase_order_id': newpurchase_order_id,
        'po' : po,
        'po_id' : po_id,
        'fo_id': fo_id,
        'q_id' : q_id,
        'status' : status,
        'cust_userID' : cust_userID,
        'cust_fullname' : cust_fullname,
        'item_list' : item_list,
    }
    return render(request,'viewpendingpo/poconfirmation.html',context)