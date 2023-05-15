from django.forms import ModelForm, forms, Select, ModelChoiceField

from app.models import PurchaseRequisition, PurchaseRequisitionItem, Item


class PurchaseRequisitionForm(ModelForm):
    class Meta:
        model = PurchaseRequisition
        fields = []


class PurchaseRequisitionItemForm(ModelForm):
    class Meta:
        model = PurchaseRequisitionItem
        fields = []


class ItemForm(ModelForm):
    # item_select = forms.ModelMultipleChoiceField(queryset=None)
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['item_select'].queryset = ...

    class Meta:
        model = Item
        fields = ['item_name']
