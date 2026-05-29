from django.db import models

# Create your models here.
from users.models import User
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey('users.Address', on_delete=models.CASCADE)

    total_price = models.FloatField()
    STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
)

    status = models.CharField(
     max_length=20,
     choices=STATUS_CHOICES,
     default='Pending'
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.product} ({self.quantity})"