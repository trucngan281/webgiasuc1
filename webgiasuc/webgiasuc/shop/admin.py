from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'date']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.OrderDetail)
admin.site.register(models.Order)
admin.site.register(models.Coupon)
