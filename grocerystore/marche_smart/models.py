from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    in_stock = models.BooleanField(default=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Owner: {self.name}"


class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Customer: {self.name}"
from django.db import models

# Create your models here.
