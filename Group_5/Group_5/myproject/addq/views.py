from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from app.models import Quotation, Quotation_Item, Purchase_Requisition, Purchase_Requisition_Item, Item
from django.contrib.auth.models import User

import numpy as np

@login_required
def showpr(request):
    prlist = Purchase_Requisition.objects.filter(purchase_requisition_status = "Pending").values()
    all_users = User.objects.all()
    context = {
        'title': 'Purchase Requisition List',
        'year': datetime.now().year,
        'prlist' : prlist,
        'all_users' : all_users
    }
    context['user'] = request.user
    return render(request,'addq/prlist.html',context)
    
def addqform(request):
    newpurchase_requisition_id= request.POST['purchase_requisition_id']    
    if (Purchase_Requisition.objects.filter(purchase_requisition_id = newpurchase_requisition_id).exists()):
        pr = Purchase_Requisition.objects.filter(purchase_requisition_id = newpurchase_requisition_id)
        cust_ID = Purchase_Requisition.objects.values_list('customer', flat=True).get(purchase_requisition_id = newpurchase_requisition_id)
        cust = User.objects.get(id = cust_ID)
        pritems = Purchase_Requisition_Item.objects.filter(purchase_requisition_id = newpurchase_requisition_id).values_list('item_id', 'item_quantity_PR')
        items = Item.objects.all().values_list('item_id', 'item_name', 'item_price')

        item_list = []
        np_pritems = np.array(list(pritems))
        np_items = np.array(list(items))

        for i in range(len(np_pritems)):
            for j in range(len(np_items)):
                if(np_pritems.T[0][i] == np_items.T[0][j]):
                    item_list.append([np_pritems.T[0][i], np_items.T[1][j], np_pritems.T[1][i], np_items.T[2][j]])

        if(pr[0].purchase_requisition_status != "Pending"):
            messages.error(request, 'Quotation of Purchase Requisition ' + newpurchase_requisition_id + ' is already completed!')
            newpurchase_requisition_id = ''
            return render(request,'addq/error.html')
    else:
        messages.error(request, 'Purchase Requisition ' + newpurchase_requisition_id + ' not found!')
        newpurchase_requisition_id = ''
        return render(request,'addq/error.html')

    context = {
        'title': 'Quotation List',
        'year': datetime.now().year,
        'purchase_requisition_id': newpurchase_requisition_id,
        'salesman' : request.user,
        'cust' : cust,
        'created_date' : datetime.now(),
        'list': item_list,
    }
    return render(request,'addq/addqform.html',context)

def addqconfirmation(request):
    id = Quotation.objects.all().count()
    index = str(id+1).zfill(5)
    newQuotation_id = "Q"+index
    
    newpurchase_requisition_id= request.POST['purchase_requisition_id']
    if (Purchase_Requisition.objects.filter(purchase_requisition_id = newpurchase_requisition_id).exists()):
        pr = Purchase_Requisition.objects.filter(purchase_requisition_id = newpurchase_requisition_id)
        cust_ID = Purchase_Requisition.objects.values_list('customer', flat=True).get(purchase_requisition_id = newpurchase_requisition_id)
        cust = User.objects.get(id = cust_ID)
        newquotation_total_price = 0

        newquotation_created_date = datetime.now()
        newquotation_expiry_date = request.POST['quotation_expiry_date']

        if(pr[0].purchase_requisition_status != "Pending"):
            messages.error(request, 'Quotation of Purchase Requisition ' + newpurchase_requisition_id + ' is already completed!')
            newpurchase_requisition_id = ''
            return render(request,'addq/error.html')
        elif(newquotation_expiry_date == ''):
            messages.error(request, 'Expiry Date is not entered!')
            return render(request,'addq/error.html')
        else:
            item_id = []
            item_quantity = []
            item_unit_price = []
            item_total_price = []
            
            i = 0
            for i in range (5):  
                newitem_id = request.POST['item_id'+str(i)]
                newitem_quantity_Q = request.POST['item_quantity_Q'+str(i)]
                newitem_unit_price = request.POST['item_unit_price_Q'+str(i)]
                if i == 0:
                    if (newitem_id != '' and newitem_quantity_Q != '' and newitem_unit_price != ''):
                        if (Item.objects.filter(item_id = newitem_id).exists()):
                            item_id.append(newitem_id)
                            item_quantity.append(newitem_quantity_Q)
                            item_unit_price.append(newitem_unit_price)
                            newitem_total_price = float(newitem_unit_price) * float(newitem_quantity_Q)
                            item_total_price.append(newitem_total_price)
                        else:
                            messages.error(request, 'Item ' + newitem_id + ' not found!')
                            return render(request,'addq/error.html')
                    elif (newitem_id == '' and newitem_quantity_Q == '' and newitem_unit_price == ''):
                        messages.error(request, 'Nothing is entered!')
                        return render(request,'addq/error.html')
                    elif (newitem_id == ''):
                        messages.error(request, 'Item ID is not entered!')
                        return render(request,'addq/error.html')
                    elif (newitem_id != ''):
                        if(newitem_quantity_Q == ''):
                            messages.error(request, 'Quantity of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/error.html')
                        else:
                            messages.error(request, 'Unit price of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/error.html')
                else:
                    if (newitem_id != '' and newitem_quantity_Q != '' and newitem_unit_price != ''):
                        if (Item.objects.filter(item_id = newitem_id).exists()):
                            item_id.append(newitem_id)
                            item_quantity.append(newitem_quantity_Q)
                            item_unit_price.append(newitem_unit_price)
                            newitem_total_price = float(newitem_unit_price) * float(newitem_quantity_Q)
                            item_total_price.append(newitem_total_price)
                        else:
                            messages.error(request, 'Item ' + newitem_id + ' not found!')
                            return render(request,'addq/error.html')
                    elif ((newitem_id == '' and newitem_quantity_Q != '') or (newitem_id == '' and newitem_unit_price != '')):
                        messages.error(request, 'Item ID is not entered!')
                        return render(request,'addq/error.html')
                    elif (newitem_id != ''):
                        if(newitem_quantity_Q == ''):
                            messages.error(request, 'Quantity of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/error.html')
                        else:
                            messages.error(request, 'Unit price of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/error.html')
    else:
        messages.error(request, 'Purchase Requisition ID is not entered!')
        return render(request,'addq/error.html')

    newquotation_total_price = sum(item_total_price)

    newq = Quotation(quotation_id = newQuotation_id,purchase_requisition_id = newpurchase_requisition_id,customer_id = cust_ID, 
                            salesman_id = request.user.id, quotation_total_price = newquotation_total_price, 
                            quotation_created_date = newquotation_created_date, quotation_expiry_date = newquotation_expiry_date)
    newq.save()

    for j in range(len(item_id)):
        newitem_id2 = Item.objects.get(item_id=item_id[j])
        
        newqitems = Quotation_Item(quotation = newq, item_id = newitem_id2, 
            item_quantity_Q = item_quantity[j], item_unit_price = item_unit_price[j], item_total_price = item_total_price[j])
        newqitems.save()

    prs = Purchase_Requisition.objects.filter(purchase_requisition_id=newpurchase_requisition_id)
    pr = prs[0]
    pr.purchase_requisition_status = "Completed"
    pr.save()

    q = Quotation.objects.get(quotation_id=newQuotation_id)

    context = {

        'quotation_id': newQuotation_id,
        'purchase_requisition_id': newpurchase_requisition_id,
        'customer_id': cust.get_username(),
        'salesman_id': request.user.get_username(),
        'quotation_total_price': q.quotation_total_price,
        'quotation_created_date': newquotation_created_date,
        'quotation_expiry_date': newquotation_expiry_date,
            
    }
    return render(request,'addq/addqconfirmation.html',context)