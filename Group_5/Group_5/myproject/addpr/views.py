from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from app.models import Item, Purchase_Requisition_Item, Purchase_Requisition


# Create your views here.
@login_required
def addprform(request):
    cust = User.objects.get(id=request.user.id)

    context = {
        'title': 'Add Purchase Requisition Form', 
        'year': datetime.now().year, 
        'user': request.user,
        'cust': cust.email
    }

    return render(request, 'addpr/addprform.html', context)


def addprconfirmation(request):
    id = Purchase_Requisition.objects.all().count()
    index = str(id + 1).zfill(5)
    newpurchase_requisition_id = "PR" + index
    newsubmitted_date = datetime.now()
    newpurchase_requisition_status = request.POST.get('purchase_requisition_status', "Pending")
    newpr = Purchase_Requisition(purchase_requisition_id=newpurchase_requisition_id, submitted_date=newsubmitted_date,
                                customer=request.user, purchase_requisition_status=newpurchase_requisition_status)
    newpr.save()

    pr_list = []
    i = 0
    for i in range(5):
        newitem_id = request.POST['item_id' + str(i)]
        newitem_quantity_PR = request.POST['item_quantity_PR' + str(i)]
        if i == 0:
            if newitem_id != '' and newitem_quantity_PR != '':
                if Item.objects.filter(item_id=newitem_id).exists():
                    newitem_id2 = Item.objects.get(item_id=newitem_id)
                    newpritems = Purchase_Requisition_Item(purchase_requisition_id=newpr, item_id=newitem_id2,
                                                         item_quantity_PR=newitem_quantity_PR)
                    newpritems.save()
                    pr_list.append(newpritems)
                else:
                    messages.error(request, 'Item ' + newitem_id + ' not found!')
                    pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                    pr.delete()
                    return render(request, 'addpr/error.html')
            elif newitem_id != '' and newitem_quantity_PR == '':
                messages.error(request, 'Quantity of ' + newitem_id + ' is not entered!')
                pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                pr.delete()
                return render(request, 'addpr/error.html')
            elif newitem_id == '' and newitem_quantity_PR != '':
                messages.error(request, 'Item ID is not entered!')
                pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                pr.delete()
                return render(request, 'addpr/error.html')
            else:
                messages.error(request, 'Nothing is entered!')
                pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                pr.delete()
                return render(request, 'addpr/error.html')
        else:
            if newitem_id != '' and newitem_quantity_PR != '':
                if Item.objects.filter(item_id=newitem_id).exists():
                    newitem_id2 = Item.objects.get(item_id=newitem_id)
                    newpritems = Purchase_Requisition_Item(purchase_requisition_id=newpr, item_id=newitem_id2,
                                                         item_quantity_PR=newitem_quantity_PR)
                    newpritems.save()
                    pr_list.append(newpritems)
                else:
                    messages.error(request, 'Item ' + newitem_id + ' not found!')
                    pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                    pr.delete()
                    return render(request, 'addpr/error.html')
            elif newitem_id != '' and newitem_quantity_PR == '':
                messages.error(request, 'Quantity of ' + newitem_id + ' is not entered!')
                pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                pr.delete()
                return render(request, 'addpr/error.html')
            elif newitem_id == '' and newitem_quantity_PR != '':
                messages.error(request, 'Item ID is not entered!')
                pr = Purchase_Requisition.objects.get(purchase_requisition_id=newpurchase_requisition_id)
                pr.delete()
                return render(request, 'addpr/error.html')

    context = {
        'purchase_requisition_id': newpurchase_requisition_id,
        'newcustomer': request.user.get_username(),
        'submitted_date': newsubmitted_date,
        'purchase_requisition_status': newpurchase_requisition_status,
        'purchase_requisition_item': pr_list
    }

    return render(request, 'addpr/addprconfirmation.html', context)


def add_customer(request):
    items = Item.objects.all()

    return render(request, 'addpr/addprform.html', {'items': items})
