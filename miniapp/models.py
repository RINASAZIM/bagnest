#models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class bag(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="image/")
    price = models.CharField(max_length=200, null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # Associate with User
    product = models.ForeignKey(bag, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1,null=True)
    

  
    def total_price(self):
     return float(self.product.price) * int(self.quantity)

    
class registerr(models.Model):
    name=models.CharField(max_length=200,null=True)
    age=models.CharField(max_length=290,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    username=models.CharField(max_length=200,null=True)
    password=models.CharField(max_length=200,null=True)

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(bag, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"