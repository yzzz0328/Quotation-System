"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User

#sharing entity  
class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=6)
    item_name = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=None,null=True,blank=True)
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)
    
class Purchase_Requisition(models.Model):
    purchase_requisition_id = models.CharField(primary_key=True, max_length=7)
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=True,default=None, blank=True, related_name ='pr_customers')
    submitted_date = models.DateField(default=None,null=True,blank=True)
    purchase_requisition_status = models.CharField(max_length=20, null=True,default="Pending", blank=True)
    def __str__(self):
        return str(self.purchase_requisition_id)

class Purchase_Requisition_Item(models.Model):
    purchase_requisition_id = models.ForeignKey(Purchase_Requisition, on_delete=models.CASCADE, null=True,default=None, blank=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True,default=None, blank=True)
    item_quantity_PR = models.IntegerField()
    def __str__(self):
        return "%s %s" % (self.purchase_requisition_id, self.item_id)
    
class Quotation(models.Model):
    quotation_id = models.CharField(primary_key=True, max_length=6)
    purchase_requisition = models.ForeignKey(Purchase_Requisition, on_delete=models.CASCADE, null=True,default=None, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE,null=True,default=None, blank=True, related_name ='q_customers')
    salesman = models.ForeignKey(User, on_delete=models.CASCADE,null=True,default=None, blank=True, related_name ='q_salesman')
    quotation_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=None,null=True,blank=True)
    quotation_created_date = models.DateField(default=None,null=True,blank=True)
    quotation_expiry_date = models.DateField(default=None,null=True,blank=True)
    def __str__(self):
        return str(self.quotation_id)

class Quotation_Item(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True,default=None, blank=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True,default=None, blank=True)
    item_quantity_Q = models.IntegerField()
    item_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=None,null=True,blank=True)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=None,null=True,blank=True)
    def __str__(self):
        return "%s %s" % (self.quotation_id, self.item_id)

class Purchase_Order(models.Model):
    purchase_order_id = models.CharField(primary_key=True, max_length=7)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, null=True,default=None, blank=True)
    finance_officer = models.ForeignKey(User, on_delete=models.CASCADE,null=True,default=None, blank=True, related_name ='po_fo')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_order_created_date = models.DateField(default=None,null=True,blank=True)
    delivery_date = models.DateField(default=None,null=True,blank=True)
    purchase_order_status = models.CharField(max_length=20, null=True,default=None, blank=True)
    def __str__(self):
        return str(self.purchase_order_id)
    
class Purchase_Order_Item(models.Model):
    purchase_order = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True,default=None, blank=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True,default=None, blank=True)
    item_quantity_PO = models.IntegerField()
    item_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=None,null=True,blank=True)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=None,null=True,blank=True)
    def __str__(self):
        return "%s %s" % (self.purchase_order_id, self.item_id)

class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True,default=None, blank=True)
    stock_quantity = models.IntegerField()
    def __str__(self):
        return "%s %s" % (self.item_id, self.stock_quantity)