"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views as main_views
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime

from additem import views as additem_views
from addpr import views as addpr_views
from addq import views as addq_views
from addpo import views as addpo_views
from viewq import views as viewq_views
from viewpo import views as viewpo_views
from viewpo_M import views as viewpo_M_views
from viewreport import views as viewreport_views
from viewstock import views as viewstock_views
from viewpendingpo import views as viewpendingpo_views
from viewpr import views as viewpr_views
from viewcq import views as viewcq_views
# from viewpo import views as viewpo_views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', main_views.home, name='home'),
    re_path(r'^contact$', main_views.contact, name='contact'),
    re_path(r'^about$', main_views.about, name='about'),
    re_path(r'^login/$',
        LoginView.as_view(template_name = 'app/login.html'),
        name='login'),
    re_path(r'^logout$',
        LogoutView.as_view(template_name = 'app/index.html'),
        name='logout'),
    re_path(r'^menu$', main_views.menu, name='menu'),

    re_path(r'^additemform$', additem_views.additemform, name='additem_form'),
    re_path(r'^additemconfirmation$', additem_views.additemconfirmation, name='additem_confirmation'),
    
    re_path(r'^addprform$', addpr_views.addprform, name='addpr_form'),
    re_path(r'^addprconfirmation$', addpr_views.addprconfirmation, name='addpr_confirmation'),
    
    re_path(r'^viewprlist$', viewpr_views.viewprlist, name='view_pr_list'),
    re_path(r'^viewpr$', viewpr_views.viewpr, name='view_pr'),

    re_path(r'^viewcqlist$', viewcq_views.viewcqlist, name='view_cq_list'),
    re_path(r'^viewcq$', viewcq_views.viewcq, name='view_cq'),

    re_path(r'^prlist$', addq_views.showpr, name='prlist_form'),
    re_path(r'^addqform$', addq_views.addqform, name='addq_form'),
    re_path(r'^addqconfirmation$', addq_views.addqconfirmation, name='addq_confirmation'),
    
    re_path(r'^qlist$', viewq_views.showq, name='qlist_form'),
    re_path(r'^viewqform$', viewq_views.viewqform, name='viewq_form'),
    
    re_path(r'^quotationlist$', addpo_views.showquotation, name='quotationlist_form'),
    re_path(r'^polist$', viewpo_views.showpo, name='polist_form'),
    re_path(r'^addpoform$', addpo_views.addpoform, name='addpo_form'),
    re_path(r'^addpoconfirmation$', addpo_views.addpoconfirmation, name='addpo_confirmation'),
    re_path(r'^viewpoform$', viewpo_views.viewpoform, name='viewpo_form'),
    
    re_path(r'^viewreport$', viewreport_views.viewreport, name='viewreport'),
    re_path(r'^showpurchaseorderreport$', viewreport_views.showpurchaseorderreport, name='showpurchaseorderreport'),
    re_path(r'^viewstock$', viewstock_views.showstock, name='viewstock'),
    re_path(r'^viewpendingpo$', viewpendingpo_views.viewpendingpo, name='viewpendingpo'),
    re_path(r'^showpendingpo$', viewpendingpo_views.showpendingpo, name='showpendingpo'),
    re_path(r'^showpoconfirmation$', viewpendingpo_views.showpoconfirmation, name='showpoconfirmation'),
    re_path(r'^viewpo_M$', viewpo_M_views.viewpo_M, name='viewpo_M'),
    re_path(r'^showpo_M$', viewpo_M_views.showpo_M, name='showpo_M'),
]
