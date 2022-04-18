from django.contrib import admin

from.models.product import Product
from.models.category import Category
from.models.customers import Customer
from.models.orders import Order

class AdminProduct(admin.ModelAdmin):
    list_display=['name','price','category','description']

class AdminCategory(admin.ModelAdmin):
    list_display=['name']

admin.site.register(Product,AdminProduct)
admin.site.register(Customer)
admin.site.register(Category,AdminCategory)
admin.site.register(Order)

# Register your models here.
