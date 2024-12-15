from django.db import models

# Create your models here.

class Ims_customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    mobile = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Ims_user(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]
    USER_TYPES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='member')
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    

class Ims_supplier(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]
    supplier_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    address = models.TextField()
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)

    def __str__(self):
        return self.supplier_name
    


class Ims_category(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name




class Ims_brand(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]
    category = models.ForeignKey(Ims_category, on_delete=models.CASCADE)
    bname = models.CharField(max_length=250)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)

    def __str__(self):
        return self.bname




class Ims_product(models.Model):
    STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]
    category_id = models.ForeignKey(Ims_category, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Ims_brand, on_delete=models.CASCADE)
    pname = models.CharField(max_length=300)
    model = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=150)
    base_price = models.FloatField() 
    tax = models.DecimalField(max_digits=4, decimal_places=2) 
    minimum_order = models.FloatField(default=0)
    supplier = models.ForeignKey(Ims_supplier, on_delete=models.CASCADE)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pname



class Ims_purchase(models.Model):
    supplier_id = models.ForeignKey('Ims_supplier', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Ims_product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_id.pname

    

class Ims_order(models.Model):
    product_id = models.ForeignKey('Ims_product', on_delete=models.CASCADE)
    total_shipped = models.IntegerField()
    customer_id = models.ForeignKey('Ims_customer', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_id.pname
