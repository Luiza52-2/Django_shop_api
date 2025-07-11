from django.db import models
from django.contrib.auth.models import User
import random

class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title  

STARS = tuple((i, '* ' * i) for i in range(1, 6))



class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=STARS, default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Отзыв на {self.product.title}"   





