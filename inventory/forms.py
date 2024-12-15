from django import forms
from .models import Ims_customer, Ims_category, Ims_brand, Ims_supplier, Ims_product, Ims_purchase, Ims_order

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Ims_customer
        fields = ['name', 'address', 'mobile', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Ims_category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Ims_brand
        fields = ['category', 'bname']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'bname': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Ims_supplier
        fields = ['supplier_name', 'mobile', 'address']
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Ims_product
        fields = ['category_id', 'brand_id', 'pname', 'model', 'description', 'quantity', 'base_price', 'tax', 'supplier']
        widgets = {
            'category_id': forms.Select(attrs={'class': 'form-control'}),
            'brand_id': forms.Select(attrs={'class': 'form-control'}),
            'pname': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Ims_purchase
        fields = ['product_id', 'quantity', 'supplier_id']
        widgets = {
            'product_id': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier_id': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Ims_order
        fields = ['product_id', 'total_shipped', 'customer_id']
        widgets = {
            'product_id': forms.Select(attrs={'class': 'form-control'}),
            'total_shipped': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_id': forms.Select(attrs={'class': 'form-control'}),
        }
