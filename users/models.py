from django.db import models




class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

   
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    

    def __str__(self):
        return self.name
    

class Wishlist(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.product.name}"