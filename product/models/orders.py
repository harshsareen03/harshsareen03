from django.db import models
from .customers import Customer
from .customers import Customer


class Order(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.IntegerField(max_length=10)
    email=models.EmailField(max_length=20)
    password=models.CharField(max_length=50)

    

    def __str__(self):
        return self.name


