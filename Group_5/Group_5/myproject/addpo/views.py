from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from app.models import Quotation, Quotation_Item, Purchase_Order, Purchase_Order_Item, Item
from django.contrib.auth.models import User
import numpy as np

@login_required
def showquotation(request):
    quotationlist = Quotation.objects.all()
    all_users = User.objects.all()
    context = {
        'title': 'Quotation List',
        'year': datetime.now().year,
        'quotationlist' : quotationlist,
        'all_users' : all_users
    }
    context['user'] = request.user
    return render(request,'addpo/quotationlist.html',context)
    
def addpoform(request):
    newquotation_id= request.POST['quotation_id']   
    if (Quotation.objects.filter(quotation_id = newquotation_id).exists()):
        q = Quotation.objects.filter(quotation_id = newquotation_id).values_list('quotation_id')
        qitems = Quotation_Item.objects.filter(quotation_id = newquotation_id).values_list('item_id', 'item_quantity_Q', 'item_total_price')
        items = Item.objects.all().values_list('item_id', 'item_name', 'item_price')

        item_list = []
        np_qitems = np.array(list(qitems))
        np_items = np.array(list(items))

        for i in range(len(np_qitems)):
            for j in range(len(np_items)):
                if(np_qitems.T[0][i] == np_items.T[0][j]):
                    item_list.append([np_qitems.T[0][i], np_items.T[1][j], np_qitems.T[1][i], np_items.T[2][j], np_qitems.T[2][i]])
    else:
        messages.error(request, 'Item ' + newquotation_id + ' not found!')
        newquotation_id = ''
        return render(request,'addpo/poerror.html')

    context = {
        'title': 'Purchase Order List',
        'year': datetime.now().year,
        'quotation_id': newquotation_id,
        'q' : q,
        'finance_officer' : request.user,
        'created_date' : datetime.now(),
        'item_list' : item_list,
    }
    return render(request,'addpo/addpoform.html',context)

def addpoconfirmation(request):
    id = Purchase_Order.objects.all().count()
    index = str(id+1).zfill(5)
    newPurchase_Order_id = "PO"+index
    
    newquotation_id= request.POST['quotation_id']
    if (Quotation.objects.filter(quotation_id = newquotation_id).exists()):
        q = Quotation.objects.filter(quotation_id = newquotation_id)
        newpurchase_order_total_price = 0

        newpurchase_order_created_date = datetime.now()
        newpurchase_order_delivery_date = request.POST['purchase_order_delivery_date']
        newpurchase_order_status = "Pending"

        if(newpurchase_order_delivery_date == ''):
            messages.error(request, 'Delivery Date is not entered!')
            return render(request,'addpo/poerror.html')
        else:
            item_id = []
            item_quantity = []
            item_unit_price = []
            item_total_price = []
            i = 0
            for i in range (5):  
                newitem_id = request.POST['item_id'+str(i)]
                newitem_quantity_PO = request.POST['item_quantity_Q'+str(i)]
                newitem_unit_price = request.POST['item_unit_price_Q'+str(i)]
                if i == 0:
                    if (newitem_id != '' and newitem_quantity_PO != '' and newitem_unit_price != ''):
                        if (Item.objects.filter(item_id = newitem_id).exists()):
                            item_id.append(newitem_id)
                            item_quantity.append(newitem_quantity_PO)
                            item_unit_price.append(newitem_unit_price)
                            newitem_total_price = float(newitem_unit_price) * float(newitem_quantity_PO)
                            item_total_price.append(newitem_total_price)
                        else:
                            messages.error(request, 'Item ' + newitem_id + ' not found!')
                            return render(request,'addpo/poerror.html')
                    elif (newitem_id == '' and newitem_quantity_PO == '' and newitem_unit_price == ''):
                        messages.error(request, 'Nothing is entered!')
                        return render(request,'addq/poerror.html')
                    elif (newitem_id == ''):
                        messages.error(request, 'Item ID is not entered!')
                        return render(request,'addq/poerror.html')
                    elif (newitem_id != ''):
                        if(newitem_quantity_PO == ''):
                            messages.error(request, 'Quantity of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/poerror.html')
                        else:
                            messages.error(request, 'Unit price of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/poerror.html')
                else:
                    if (newitem_id != '' and newitem_quantity_PO != '' and newitem_unit_price != ''):
                        if (Item.objects.filter(item_id = newitem_id).exists()):
                            item_id.append(newitem_id)
                            item_quantity.append(newitem_quantity_PO)
                            item_unit_price.append(newitem_unit_price)
                            newitem_total_price = float(newitem_unit_price) * float(newitem_quantity_PO)
                            item_total_price.append(newitem_total_price)
                        else:
                            messages.error(request, 'Item ' + newitem_id + ' not found!')
                            return render(request,'addpo/poerror.html')
                    elif ((newitem_id == '' and newitem_quantity_PO != '') or (newitem_id == '' and newitem_unit_price != '')):
                        messages.error(request, 'Item ID is not entered!')
                        return render(request,'addq/poerror.html')
                    elif (newitem_id != ''):
                        if(newitem_quantity_PO == ''):
                            messages.error(request, 'Quantity of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/poerror.html')
                        else:
                            messages.error(request, 'Unit price of ' + newitem_id + ' is not entered!')
                            return render(request,'addq/poerror.html')
    else:
        messages.error(request, 'Quotation ID is not entered!')
        return render(request,'addpo/poerror.html')

    newpurchase_order_total_price = sum(item_total_price)

    newpo = Purchase_Order(purchase_order_id = newPurchase_Order_id,quotation_id = newquotation_id, 
                            finance_officer_id = request.user.id, total_price = newpurchase_order_total_price, 
                            purchase_order_created_date = newpurchase_order_created_date, 
                            delivery_date = newpurchase_order_delivery_date, purchase_order_status=newpurchase_order_status)
    newpo.save()

    for j in range(len(item_id)):
        newitem_id2 = Item.objects.get(item_id=item_id[j])
        
        newpoitems = Purchase_Order_Item(purchase_order = newpo, item_id = newitem_id2, 
            item_quantity_PO = item_quantity[j], item_unit_price = item_unit_price[j], item_total_price = item_total_price[j])
        newpoitems.save()

    qs = Quotation.objects.filter(quotation_id=newquotation_id)
    q = qs[0]
    q.save()

    po = Purchase_Order.objects.get(purchase_order_id=newPurchase_Order_id)

    context = {

        'purchase_order_id': newPurchase_Order_id,
        'quotation_id': newquotation_id,
        'finance_officer_id': request.user.get_username(),
        'total_price': po.total_price,
        'purchase_order_created_date': newpurchase_order_created_date,
        'delivery_date': newpurchase_order_delivery_date,
        'purchase_order_status' : newpurchase_order_status,
            
    }
    return render(request,'addpo/addpoconfirmation.html',context)