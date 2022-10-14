import uuid
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=2083, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=2083)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ManyToManyField(Category, related_name='products')


    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(datetime.now, editable=False, null=True)
    timestamp = models.DateTimeField(auto_now=True, editable=False, null=True)


    @property
    def get_cart_total(self):
        orderitems = self.order_items.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_items_total(self):
        orderitems = self.order_items.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

    def __str__(self):
        return self.product.name


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=300, null=False)
    state = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address