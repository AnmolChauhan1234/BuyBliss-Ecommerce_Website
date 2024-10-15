from django.shortcuts import render, redirect
from .models import Product,Contact,Order, Cart, cartItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from math import ceil
import json
from decimal import Decimal

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

# def cart(request):
#     return render(request, 'shop/cart.html')

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
                # If password is not wrong password
                login(request, user)
                # messages.success(request, "Successfully Logged In")
                # return redirect('/shop')
                return JsonResponse({'status': 'success', 'message': 'Login successfull'})
            else:
                # messages.error(request, "Invalid credentials! Please try again")
                # return redirect("/shop")
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials! Please try again'})
        except User.DoesNotExist:
            # If no object or more than one object is found, get() will raise exceptions (DoesNotExist or MultipleObjectsReturned).
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


def view_cart(request):
    # Initialize cart as empty
    cart = {}

    if request.user.is_authenticated:
        try:
            # Fetch the cart for the authenticated user
            cart_instance = Cart.objects.get(user=request.user)
            cart_items = cartItem.objects.filter(cart=cart_instance)

            for item in cart_items:
                cart[item.product.id] = [
                    item.quantity,
                    item.product.product_name,              # Here product is instance of Product created in cartItem model
                    item.product.image.url, 
                    item.product.price, 
                    item.product.desc, 
                    item.product.product_brand,
                    item.product.category,
                ]

            # Check if the request is an AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'cart': cart})

            # Render the cart page template for authenticated users
            return render(request, 'shop/cart.html', {'cart': cart})

        except Cart.DoesNotExist:
            # Handle the case where the cart does not exist
            return render(request, 'shop/cart.html', {'cart': {}})  # Render empty cart template

    # If the user is not logged in, render the cart page template with an empty cart
    return render(request, 'shop/cart.html', {'cart': {}})  # Render empty cart template


    
        

# def add_to_crt(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         data = json.loads(request.body)
#         product_id = data.get('productId')
#         quantity = data.get('quantity',1)
#         cart_instance = Cart.objects.get(user=request.user)
#         cart_item = Cart.objects.get(cart=cart_instance, product_id=product_id)

# def update_cartItem(request):
#     if request.method == 'POST' and request.user.is_authenticated:
#         data = json.loads(request.body)
#         print("Raw body:", request.body)  # Debugging the raw request body
#         print("Data received:", data)
#         product_id = int(data.get('productId'))
#         quantity = int(data.get('quantity'))
#         print("Product ID:", product_id)
#         print("Quantity:", quantity)


#         try:
#             # Get or create the user's cart
#             cart_instance, created = Cart.objects.get_or_create(user=request.user)
#             # The created variable stores a boolean value.

#             # If a new Cart instance is created (because there wasn’t one already associated with the user), created will be True.
#             # If an existing Cart is found for the user, created will be False.


#             # Get or create the cart item linked to the cart_instance
#             # If the item does not exist (i.e., this is a new product being added), a new cartItem instance is created, and the variable item_created is set to True.
#             product = Product.objects.get(id=product_id)
#             cart_item, item_created = cartItem.objects.get_or_create(cart=cart_instance, product=product)
#             # Use cart=cart_instance to link the item to the user's cart
#             # Here, product is the actual Product instance, retrieved using Product.objects.get(id=product_id).
#             # When you call get_or_create(), you pass the cart_instance and the product object. This approach is correct according to your model because the cartItem model expects a product (an instance of the Product model) in the ForeignKey field.
#             product_price = Decimal(product.price)
#             if product_price == Decimal('0.00'):
#                 return JsonResponse({'success': False, 'error': 'Product price is zero or invalid'})

#             if item_created:
#             # cart_item is the model instance you are modifying.
#             # item_created is only a flag, so you don't assign any values to it; it just indicates whether the item was newly created.
#                 cart_item.quantity = quantity
#             else:
#                 cart_item.quantity += quantity

#             cart_item.save()

#             print("Cart item updated:", cart_item)  # Debugging the cart item
#             return JsonResponse({'success': True})

#         except Product.DoesNotExist:
#             print("Error: Product not found")  # Debugging missing product
#             return JsonResponse({'success': False, 'error': 'Product not found'})

#         except Exception as e:
#             print("Error:", str(e))  # Log any other errors
#             return JsonResponse({'success': False, 'error': str(e)})

#     print("Error: Invalid request or user not authenticated")  # Log unauthenticated request
#     return JsonResponse({'success': False, 'error': 'Invalid request or user not authenticated'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, cartItem, Product
from decimal import Decimal
import json

@csrf_exempt
def update_cartItem(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            print("Data received:", data)
            
            product_id = int(data.get('productId'))
            quantity = int(data.get('quantity'))

            # Get or create the user's cart
            cart_instance, created = Cart.objects.get_or_create(user=request.user)

            # Get the product by ID
            product = Product.objects.get(id=product_id)
            print("Product retrieved:", product)

            # Convert product price to Decimal and check for zero price
            product_price = Decimal(product.price)
            print("Converted product price:", product_price)

            # Ensure price is valid (non-zero)
            if product_price == Decimal('0.00'):
                print("Error: Product price is zero")
                return JsonResponse({'success': False, 'error': 'Product price is zero and cannot be added to the cart'})

            # Get or create the cart item
            cart_item, item_created = cartItem.objects.get_or_create(cart=cart_instance, product=product)

            # Update quantity and price immediately
            if item_created:
                cart_item.quantity = quantity
                cart_item.price = product_price  # Set the correct price for new items
            else:
                cart_item.quantity += quantity
                cart_item.price = product_price  # Update price for existing items if needed

            print(f"Setting cart item price to {cart_item.price}")
            cart_item.save()

            print("Cart item updated:", cart_item)
            return JsonResponse({'success': True})

        except Product.DoesNotExist:
            print("Error: Product not found")
            return JsonResponse({'success': False, 'error': 'Product not found'})

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})

    print("Error: Invalid request or user not authenticated")
    return JsonResponse({'success': False, 'error': 'Invalid request or user not authenticated'})


def updateCart(request):
    if request.user.is_authenticated:
        try:
            cart_instance = Cart.objects.get(user = request.user)
            cart_items = cartItem.objects.filter(cart = cart_instance)

            cart = {}

            for item in cart_items:
                cart[f'pr{item.product.id}'] = [
                    item.quantity, 
                item.product.product_name,            # Here product is instance of Product created in cartItem model
                item.product.image.url, 
                item.product.price, 
                item.product.desc, 
                item.product.product_brand,
                item.product.category,
                ]
            return JsonResponse({'cart': cart})
        except Cart.DoesNotExist:
            return JsonResponse({'cart': {}})
    return JsonResponse({'cart': {}})


def decreaseQuantity(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        print(data)
        print(item_id)

        cart = Cart.objects.get(user=request.user)
        cart_item = cartItem.objects.get(cart=cart,product_id=item_id)

        if (cart_item.quantity > 0):
            cart_item.quantity -= 1

        cart_item.save()


def increaseQuantity(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        item_id = data.get('item_id')

        cart = Cart.objects.get(user=request.user)
        cart_item = cartItem.objects.get(cart=cart,product_id=item_id)

        cart_item.quantity += 1

        cart_item.save()