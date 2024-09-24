from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50,default="")
    product_brand=models.CharField(max_length=50,default="")
    category=models.CharField(max_length=50,default="")                
    # here default="" means that - before adding a product details in your admin (add product) , by default you will see category = "" (empty string)
    subcategory=models.CharField(max_length=50,default="",blank=True)
    # here blank=True means that - you can leave subcategory as blank
    price=models.IntegerField(default=0)
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