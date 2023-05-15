from django import forms
from app.models import Purchase_Order

class POForm(forms.ModelForm):

    class Meta:
        model = Purchase_Order
        fields = ['purchase_order_id','quotation_id','finance_officer_id','total_price','purchase_order_created_date','delievery_date','purchase_order_status']
