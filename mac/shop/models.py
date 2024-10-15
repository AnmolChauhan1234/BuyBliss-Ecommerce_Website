from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    # In Django, the AutoField is used as a primary key by default unless you specify otherwise. 
    product_name=models.CharField(max_length=50,default="")
    product_brand=models.CharField(max_length=50,default="")
    category=models.CharField(max_length=50,default="")                
    # here default="" means that - before adding a product details in your admin (add product) , by default you will see category = "" (empty string)
    subcategory=models.CharField(max_length=50,default="",blank=True)
    # here blank=True means that - you can leave subcategory as blank
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True) 
    name=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=80,default="")               
    phone=models.CharField(max_length=80,default="")
    desc=models.CharField(max_length=400,default="")

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    items_json= models.CharField(max_length=5000)
    name = models.CharField(max_length = 80)
    email = models.CharField(max_length = 80)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 80)
    state = models.CharField(max_length = 80)
    zip_code = models.CharField(max_length = 80)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.order_id} by {self.name}"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class cartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal('0.00'))
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

    def save(self, *args, **kwargs):
        # Add a debug statement to print the price before saving
        print(f"Saving cartItem for {self.product.product_name} with price: {self.price}")
        
        # Temporarily remove the validation for debugging
        # if self.price == Decimal('0.00'):
        #     raise ValueError("Price cannot be zero when saving a cart item")

        # Calculate the total price
        self.total_price = self.quantity * self.price if self.price and self.quantity else Decimal('0.00')

        # Save the cart item
        super(cartItem, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product.product_name} in {self.cart.user.username}'s cart"
    
    