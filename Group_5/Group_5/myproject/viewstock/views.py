from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from app.models import Stock

# Create your views here.

@login_required
def showstock(request):
    stocklist = Stock.objects.all()
    
    context = {
        'title': 'Quotation List',
        'year': datetime.now().year,
        'stocklist' : stocklist,
    }
    context['user'] = request.user
    return render(request,'viewstock/viewstock.html',context)
    