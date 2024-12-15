from django.contrib import admin

from .models import Ims_customer, Ims_user, Ims_supplier, Ims_category, Ims_brand, Ims_product, Ims_purchase, Ims_order


# Register your models here.

admin.site.register(Ims_customer)
admin.site.register(Ims_user)
admin.site.register(Ims_supplier)
admin.site.register(Ims_category)
admin.site.register(Ims_brand)
admin.site.register(Ims_product)
admin.site.register(Ims_purchase)
admin.site.register(Ims_order)