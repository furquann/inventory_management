from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse

from .models import Ims_customer, Ims_user, Ims_supplier, Ims_category, Ims_brand, Ims_product, Ims_purchase, Ims_order
from .forms import CustomerForm, CategoryForm, BrandForm, SupplierForm, ProductForm, PurchaseForm, OrderForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from urllib.parse import urlparse
from django.core.exceptions import ObjectDoesNotExist

#login
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render

#VARIABLES
number_of_items = 10


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            print("Login Successful..")
            return redirect('home')
        else:
            print("Invalid Credentials")
            return redirect('login')
        
    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        print("Logout from Website...")
        return redirect('login')




@login_required(login_url="login")
def home(request):
    # product_tnames = Ims_product.objects.values_list('ptname', flat=True)
    products = Ims_product.objects.all()
    orders = Ims_order.objects.all()

    for product in products:
        total_shipped = sum(order.total_shipped for order in orders if order.product_id == product.id)
        product.inventories_left = product.quantity - total_shipped

    context = {
        'products': products,
        'orders': orders,
    }
    return render(request, 'home.html', context)



@login_required(login_url="login")
def customer(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        balance = request.POST.get('balance')
        address = request.POST.get('address')

        new_customer = Ims_customer(name=name, mobile=mobile, balance=balance, address=address)
        new_customer.save()
        return redirect(reverse('customer'))
    

    customers = Ims_customer.objects.all().order_by('id')

    paginated_customers = paginate(request, customers, items_per_page=number_of_items)

    return render(request, 'customer.html', {'customers': paginated_customers})



@login_required(login_url="login")
def category(request):

    if request.method == "POST":
        name = request.POST.get('name')

        new_category = Ims_category(name=name)
        new_category.save()
        return redirect(reverse('category'))
    
    categories = Ims_category.objects.all()
    paginated_categories = paginate(request, categories, items_per_page=number_of_items)


    return render(request, 'category.html', {'categories' : paginated_categories})




@login_required(login_url="login")
def brand(request):

    if request.method == "POST":
        category_name = request.POST.get('category')
        name = request.POST.get('name')

        category = Ims_category.objects.get(name=category_name)

        new_brand = Ims_brand(category=category, bname=name)
        new_brand.save()
        return redirect(reverse('brand'))

    brands = Ims_brand.objects.all()
    paginated_brands = paginate(request, brands, items_per_page=number_of_items)
    categories = Ims_category.objects.all()
    context = {
        'brands': paginated_brands,
        'categories': categories,
    }
    return render(request, 'brand.html', context)



@login_required(login_url="login")
def supplier(request):

    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        new_supplier = Ims_supplier(supplier_name=name, mobile=mobile, address=address)
        new_supplier.save()
        return redirect(reverse('supplier'))

    suppliers = Ims_supplier.objects.all()
    paginated_suppliers = paginate(request, suppliers, items_per_page=number_of_items)
    return render(request, 'supplier.html', {'suppliers': paginated_suppliers})




@login_required(login_url="login")
def product(request):

    if request.method == "POST":
        category_name = request.POST.get('category')
        brand_name = request.POST.get('brand')
        pname = request.POST.get('pname')
        model = request.POST.get('model')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        base_price = request.POST.get('base_price')
        tax = request.POST.get('tax')
        supplier_name = request.POST.get('supplier')

        new_product = Ims_product(
            category_id = Ims_category.objects.get(name=category_name),
            brand_id = Ims_brand.objects.get(bname=brand_name),
            pname = pname,
            model = model,
            description = description,
            quantity = quantity,
            base_price = base_price,
            tax = tax,
            supplier = Ims_supplier.objects.get(supplier_name=supplier_name)
        )
        new_product.save()

        return redirect(reverse('product'))

    products = Ims_product.objects.all()
    paginated_products = paginate(request, products, items_per_page=number_of_items)
    categories = Ims_category.objects.all()
    brands = Ims_brand.objects.all()
    suppliers = Ims_supplier.objects.all()

    context = {
        'products': paginated_products,
        'categories':categories,
        'brands': brands,
        'suppliers': suppliers,
    }
    return render(request, 'product.html', context)




@login_required(login_url="login")
def purchase(request):

    if request.method == "POST":
        product_name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        supplier_name = request.POST.get('supplier')

        new_purchase = Ims_purchase(
            product_id = Ims_product.objects.get(pname=product_name),
            quantity=quantity,
            supplier_id = Ims_supplier.objects.get(supplier_name=supplier_name),
        )
        new_purchase.save()

    purchases = Ims_purchase.objects.all()
    paginated_purchases = paginate(request, purchases, items_per_page=number_of_items)
    suppliers = Ims_supplier.objects.all()
    products = Ims_product.objects.all()
    context = {
        'purchases': paginated_purchases,
        'products': products,
        'suppliers': suppliers,
    }
    return render(request, 'purchase.html', context)


@login_required(login_url="login")
def orders(request):

    if request.method == "POST":
        product_name = request.POST.get('name')
        total_item = request.POST.get('total_item')
        customer_name = request.POST.get('cname')

        new_order = Ims_order(
            product_id = Ims_product.objects.get(pname=product_name),
            total_shipped = total_item,
            customer_id = Ims_customer.objects.get(name=customer_name)
        )
        new_order.save()

    orders = Ims_order.objects.all()
    paginated_orders = paginate(request, orders, items_per_page=number_of_items)
    products = Ims_product.objects.all()
    customers = Ims_customer.objects.all()
    context = {
        'orders': paginated_orders,
        'products': products,
        'customers': customers,
    }
    return render(request, 'order.html', context)








#Pagination handling
@login_required(login_url="login")
def paginate(request, tname, items_per_page=1):
    
    page_num = request.GET.get('page')
    paginator = Paginator(tname, items_per_page)

    try:
        paginated_view = paginator.page(page_num)
    except PageNotAnInteger:
        paginated_view = paginator.page(1)
    except EmptyPage:
        paginated_view = paginator.page(paginator.num_pages)

    return paginated_view




@login_required(login_url="login")
def delete(request, id):
    link = request.META.get('HTTP_REFERER')
    cropped_order = None

    try:
        if link:
            parsed_url = urlparse(link)
            cropped_order = parsed_url.path.split('/')[-2]

            if cropped_order == 'customer':
                item = Ims_customer.objects.get(id=id)
            elif cropped_order == 'category':
                item = Ims_category.objects.get(id=id)
            elif cropped_order == 'brand':
                item = Ims_brand.objects.get(id=id)
            elif cropped_order == 'supplier':
                item = Ims_supplier.objects.get(id=id)
            elif cropped_order == 'product':
                item = Ims_product.objects.get(id=id)
            elif cropped_order == 'purchase':
                item = Ims_purchase.objects.get(id=id)
            elif cropped_order == 'order':
                item = Ims_order.objects.get(id=id)
            else:
                pass

        item.delete()
    except ObjectDoesNotExist:
        pass
    
    return redirect(cropped_order)



@login_required(login_url="login.html")
def edit(request, id):
    link = request.META.get('HTTP_REFERER')
    cropped_order = None

    try:
        if link:
            parsed_url = urlparse(link)
            cropped_order = parsed_url.path.split('/')[-2]

            if cropped_order == 'customer':
                model = Ims_customer
                form_class = CustomerForm
                template_name = "customer.html"
                redirect_name = "customer"

            elif cropped_order == 'category':
                model = Ims_category
                form_class = CategoryForm
                template_name = "category.html"
                redirect_name = "category"
                
            elif cropped_order == 'brand':
                model = Ims_brand
                form_class = BrandForm
                template_name = "brand.html"
                redirect_name = "brand"

            elif cropped_order == 'supplier':
                model = Ims_supplier
                form_class = SupplierForm
                template_name = "supplier.html"
                redirect_name = "supplier"

            elif cropped_order == 'product':
                model = Ims_product
                form_class = ProductForm
                template_name = "product.html"
                redirect_name = "product"

            elif cropped_order == 'purchase':
                model = Ims_purchase
                form_class = PurchaseForm
                template_name = "purchase.html"
                redirect_name = "purchase"

            elif cropped_order == 'order':
                model = Ims_order
                form_class = OrderForm
                template_name = "order.html"
                redirect_name = "order"

            else:
                pass


        obj = get_object_or_404(model, id=id)
    
        if request.method == 'POST':
            form = form_class(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect(reverse(redirect_name))
        else:
            form = form_class(instance=obj)
        
        return render(request, template_name, {'form': form})

    except ObjectDoesNotExist:
        pass

    return return_to_page(cropped_order)



#this function redirects user to the page where the link is requested for delete and edit function
@login_required(login_url="login")
def return_to_page(cropped_order):
    if cropped_order == 'customer':
        return redirect(reverse('customer'))
    elif cropped_order == 'category':
        return redirect(reverse('category'))
    elif cropped_order == 'brand':
        return redirect(reverse('brand'))
    elif cropped_order == 'supplier':
        return redirect(reverse('supplier'))
    elif cropped_order == 'product':
        return redirect(reverse('product'))
    elif cropped_order == 'purchase':
        return redirect(reverse('purchase'))
    elif cropped_order == 'order':
        return redirect(reverse('orders'))
    else:
        pass



#all search funtions
@login_required(login_url="login")
def search_customers(request):
    if request.method == "GET":
        query = request.GET.get('query')
        return searchBar(request, Ims_customer, "customer", query, "name")


@login_required(login_url="login")
def search_category(request):
    if request.method == "GET":
        query = request.GET.get('query')
    
        if query:
                searched_items = Ims_category.objects.filter(name__contains=query)
                content = {
                    "categories": searched_items,
                }
                return render(request, f'category.html', content)
        else:
            print("No products found to show in database")
            return render(request, f'category.html', {})
    

@login_required(login_url="login")
def search_brand(request):
    if request.method == "GET":
        query = request.GET.get('query')
        return searchBar(request, Ims_brand, "brand", query, "bname")
    

@login_required(login_url="login")
def search_supplier(request):
    if request.method == "GET":
        query = request.GET.get('query')
        return searchBar(request, Ims_supplier, "supplier", query, "supplier_name")
    

@login_required(login_url="login")
def search_product(request):
    if request.method == "GET":
        query = request.GET.get('query')
        return searchBar(request, Ims_product, "product", query, "pname")
    

@login_required(login_url="login")
def search_purchase(request):
    if request.method == "GET":
        query = request.GET.get('query')
        return searchBar(request, Ims_purchase, "purchase", query, "product_id__pname")
    

@login_required(login_url="login")
def search_order(request):
    if request.method == "GET":
        query = request.GET.get('query')
        return searchBar(request, Ims_order, "order", query, "product_id__pname")


@login_required(login_url="login")
def searchBar(request, t_name, temp_name, query, s_name):
        if query:
            to_search = {s_name + '__contains': query}
            searched_items = t_name.objects.filter(**to_search)
            content = {
                f"{temp_name}s": searched_items,
            }
            return render(request, f'{temp_name}.html', content)
        else:
            print("No products found to show in database")
            return render(request, f'{temp_name}.html', {})