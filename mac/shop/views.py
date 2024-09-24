from django.shortcuts import render
from .models import Product,Contact,Order
from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds,'active_page':'index'}      # {'active_page':'index'}  here this is used to set active class on the template which is opened
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html',{'active_page':'about'})     # {'active_page':'about'}  here this is used to set active class on the template which is opened

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return render(request, 'shop/contact.html',{'active_page':'contact'})

def tracker(request):
    return render(request, 'shop/tracker.html',{'active_page':'tracker'})

def search(request):
    return render(request, 'shop/search.html')

def productView(request,myid):
    # Fetch the product using id
    product = Product.objects.filter(id=myid)     # It returns a QuerySet  (QuerySet is like a list of objects)
    print(product)
    return render(request,'shop/productview.html',{'product_tobeshown':product[0]})     # Only one object is there. So to access it product[0] is used

def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','') + request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        order=Order(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        order.save()
    return render(request, 'shop/checkout.html')
def cart(request):
    return render(request, 'shop/cart.html')

