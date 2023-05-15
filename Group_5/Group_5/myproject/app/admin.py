from django.contrib import admin
from app.models import Item, Purchase_Requisition, Purchase_Requisition_Item, Quotation, Quotation_Item, Purchase_Order, Purchase_Order_Item, Stock

admin.site.register(Item)
admin.site.register(Purchase_Requisition)
admin.site.register(Purchase_Requisition_Item)
admin.site.register(Quotation)
admin.site.register(Quotation_Item)
admin.site.register(Purchase_Order)
admin.site.register(Purchase_Order_Item)
admin.site.register(Stock)