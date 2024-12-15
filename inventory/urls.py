from django.urls import path
from django.contrib import admin

from inventory import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('customer/', views.customer, name='customer'),      
    path('category/', views.category, name='category'),       
    path('brand/', views.brand, name='brand'),          
    path('supplier/', views.supplier, name='supplier'),     
    path('product/', views.product, name='product'),       
    path('purchase/', views.purchase, name='purchase'),      
    path('orders/', views.orders, name='orders'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('search_customers/', views.search_customers, name="search_customers"),
    path('search_category/', views.search_category, name='search_category'),
    path('search_brand/', views.search_brand, name='search_brand'),
    path('search_supplier/', views.search_supplier, name='search_supplier'),
    path('search_product/', views.search_product, name='search_product'),
    path('search_purchase/', views.search_purchase, name='search_purchase'),
    path('search_order/', views.search_order, name='search_order'),

]
