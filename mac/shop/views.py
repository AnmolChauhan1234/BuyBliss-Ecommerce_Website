from django.shortcuts import render, redirect
from .models import Product,Contact,Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.http import JsonResponse
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

def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST.get('username','')
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('signupEmail','')
        pass1 = request.POST.get('signupPassword','')
        pass2 = request.POST.get('confirmPassword','')

        # check for errorneous input
        if len(username) > 10:
            # messages.error(request, "Username must be under 20 characters")
            # return redirect("/shop")
            return JsonResponse({'status': 'error', 'message': 'Username must be under 10 characters'})
        if not username.isalnum():
            # messages.error(request, "Username should only contain letters and numbers")
            # return redirect("/shop")
            return JsonResponse({'status': 'error', 'message': 'Username should only contain letters and numbers'})
        if pass1 != pass2:
            # messages.error(request, "Passwords doesn't match")
            # return redirect("/shop")
            return JsonResponse({'status': 'error', 'message': "Passwords don't match"})


        # Create the user
        myUser = User.objects.create_user(username,email,pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()

        # messages.success(request, "Your account has been succesfully created")
        # return redirect('/shop')
        return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
    
    else:
        # return HttpResponse('404 - Not found')
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
        
    

def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginemail = request.POST.get('loginEmail','')
        loginpassword = request.POST.get('loginPassword','')

        try:
            user = User.objects.get(email=loginemail)
            user = authenticate(username=user.username,password=loginpassword)
            if user is not None:
                login(request, user)
                # messages.success(request, "Successfully Logged In")
                # return redirect('/shop')
                return JsonResponse({'status': 'success', 'message': 'Login successfull'})
            else:
                # messages.error(request, "Invalid credentials! Please try again")
                # return redirect("/shop")
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials! Please try again'})
        except User.DoesNotExist:
            # If no user is found with the provided email
            # messages.error(request, "Email not found! Please try again")
            # return redirect("/shop")
            return JsonResponse({'status': 'error', 'message': 'Email not found! Please try again'})
    # return HttpResponse("404- Not found")
    return JsonResponse({'status': 'error', 'message': '404- Not found'})

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('/shop')





