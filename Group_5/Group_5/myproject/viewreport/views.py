from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from app.models import Purchase_Order, Quotation, Purchase_Order_Item, Item
from django.db.models import Sum
from django.contrib.auth.models import User
import numpy as np
# Create your views here.

@login_required
def viewreport(request):
    context = {
        'title': 'View Purchase Order Report',
        'year': datetime.now().year,
    }
    context['user'] = request.user
    return render(request,'viewreport/viewreport.html',context)

def showpurchaseorderreport(request):
    newstart_date = request.GET['start_date']
    newend_date = request.GET['end_date']
    
    p_data = Purchase_Order.objects.filter(purchase_order_created_date__range=(newstart_date, newend_date)).values()
    
    if not p_data:
        messages.error(request, 'No purchase order created!')
        return render(request,'viewreport/error.html')
    else:
        purchase_order_data = Purchase_Order.objects.filter(purchase_order_created_date__range=(newstart_date, newend_date)).values_list('purchase_order_id', 'quotation_id', 'total_price', 'purchase_order_status')
        #purchase_order_id, quotation_id, total_price, purchase_order_status
        numpy_po_data_array = np.array(list(purchase_order_data))
        numpy_quotation_id = numpy_po_data_array.T[1]
        
        salesman_id_query = Quotation.objects.filter(quotation_id__in = numpy_quotation_id).values_list('salesman_id')
        salesman_quotation_id_query = Quotation.objects.filter(quotation_id__in = numpy_quotation_id).values_list('quotation_id','salesman_id','quotation_total_price')
        numpy_salesman_quotation_id_query_array = np.array(list(salesman_quotation_id_query))
        
        temp_numpy_salesman_id_query_array = np.array(list(salesman_id_query))
        salesman_data = User.objects.filter(id__in = temp_numpy_salesman_id_query_array).values_list('username', 'first_name', 'last_name','id')
        numpy_salesman_data_array = np.array(list(salesman_data))
        numpy_salesman_first_name_array = numpy_salesman_data_array.T[1]
        numpy_salesman_last_name_array = numpy_salesman_data_array.T[2]
        numpy_salesman_id_array = numpy_salesman_data_array.T[0]
        
        salesman = []
        temp = []
        for i in range(len(numpy_salesman_data_array)):
            temp_sales = 0
            for j in range (len(numpy_salesman_quotation_id_query_array)):
                if (int(numpy_salesman_data_array.T[3][i]) == int(numpy_salesman_quotation_id_query_array.T[1][j])):
                    temp_sales += int(numpy_salesman_quotation_id_query_array.T[2][j])
            temp.append(temp_sales)
            salesman.append([numpy_salesman_id_array[i], numpy_salesman_first_name_array[i] + ' ' + numpy_salesman_last_name_array[i], temp_sales])

        salesman_total_sales = max(s[2] for s in salesman)
        index_topsales = temp.index(salesman_total_sales)
        salesman_name = salesman[1][index_topsales]
        
        p_order_items = Purchase_Order_Item.objects.filter(purchase_order_id__in = numpy_po_data_array.T[0] ).values_list('item_id_id', 'item_quantity_PO', 'item_total_price')
        numpy_p_order_items_array = np.array(list(p_order_items))
        item_list = Item.objects.filter(item_id__in = numpy_p_order_items_array.T[0]).values_list('item_id', 'item_name')
        numpy_item_list_array = np.array(list(item_list))
        
        items = []
        temp_q_list = []
        temp_q = 0
        temp_p = 0
        
        for b in range(len(numpy_item_list_array.T[0])):
            for a in range(len(numpy_p_order_items_array.T[0])):
                if (numpy_item_list_array.T[0][b] == numpy_p_order_items_array.T[0][a]):
                    temp_q += int(numpy_p_order_items_array.T[1][a])
                    temp_p += float(numpy_p_order_items_array.T[2][a])
            temp_q_list.append(temp_q)
            items.append([numpy_item_list_array.T[0][b],numpy_item_list_array.T[1][b],temp_q,temp_p])
            
        max_q = max(l[2] for l in items)
        index = temp_q_list.index(max_q)
        max_i = numpy_item_list_array.T[1][index]
        if list(p_data.filter(purchase_order_status="Approved").aggregate(Sum('total_price')).values())[0] is None:
            total_sales = 0
        else:
            total_sales = list(p_data.filter(purchase_order_status="Approved").aggregate(Sum('total_price')).values())[0]
        
        context = {
            'start_date' : newstart_date,
            'end_date' : newend_date,
            'data' : p_data,
            'user' : request.user,
            'salesman' : salesman,
            'items' : items,
            'purchase_order_id' : numpy_po_data_array.T[0],
            'purchase_order_status' : numpy_po_data_array.T[3],
            'purchase_order_total_price' : numpy_po_data_array.T[2],
            'p_order_items':p_order_items,
            'top_product': max_i,
            'top_product_q' : max_q,
            'salesman_name' : salesman_name,
            'salesman_total_sales' : salesman_total_sales,
            'a' : len(purchase_order_data.filter(purchase_order_status="Approved")),
            'b' : len(purchase_order_data.filter(purchase_order_status="Rejected")),
            'c' : len(purchase_order_data.filter(purchase_order_status="Pending")),
            'x' : len(purchase_order_data),
            'total_sales' : total_sales
        }
    
    return render(request,'viewreport/viewpurchaseordereport.html',context)