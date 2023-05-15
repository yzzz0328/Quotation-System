from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from django.contrib.auth.decorators import login_required

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    else:
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contacting Us',
            'message1':'Chang Siu Hong',
            'role1' : 'Team Leader',
            'message2':'Teo Yih Shing',
            'role2' : 'Team Member',
            'message3':'Teoh Ye Zhian',
            'message4':'Lam Ting Le',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Quotation System',
            'message':'Our quotation system will lead the user to the specified menu page according to their user types which are Customer, Salesman, Finance Officer and Manager. \n\nFor customers, our system will allow them to submit purchase requisition by inputting the relevant information and view the purchase requisition that they have submitted to check the status. The customer may also view quotations created from their purchase requisition. For salesmen, our system will allow them to create quotations based on the purchase requisition submitted to the system. Besides, the system will also allow the salesman to view the quotations they have submitted and to view stock as they will have to check on the product availability upon receiving purchase orders physically. The finance officer can perform several functions in our system which are to submit purchase orders and view past purchase orders. For managers, our system will allow them to view past purchase orders, approve or reject pending purchase orders by viewing pending purchase order lists, generate purchase order reports based on the dates inputted by the manager and display them to the manager as well as to view stock.',
            'year':datetime.now().year,
        }
    )

@login_required
def menu(request):
    check_employee = request.user.groups.filter(name='employee').exists()
    check_customer = request.user.groups.filter(name='customer').exists()
    check_salesman = request.user.groups.filter(name='salesman').exists()
    check_finance_officer = request.user.groups.filter(name='finance officer').exists()
    check_manager = request.user.groups.filter(name='manager').exists()

    context = {
            'title':'Main Menu',
            'is_employee': check_employee,
            'is_customer': check_customer,
            'is_salesman': check_salesman,
            'is_finance_officer': check_finance_officer,
            'is_manager': check_manager,
            'year':datetime.now().year,
        }
    context['user'] = request.user

    return render(request,'app/menu.html',context)