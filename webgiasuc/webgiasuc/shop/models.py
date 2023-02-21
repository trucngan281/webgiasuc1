from decimal import Decimal
from django.conf import settings
from django.db import models
from account.models import Customer
from author.models import AuthorProfile


class Category(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='products_category')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='products')
    price = models.IntegerField()
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def get_current_quantity(self, user):

        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs.first()
            qs = order.lineOrder.filter(item__pk=self.pk)
            if qs.exists():
                return qs[0].quantity

        return 0


class Coupon(models.Model):
    code = models.CharField(max_length=5)
    discount_value = models.IntegerField(default=0)


class OrderDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveSmallIntegerField(default=1)
    description = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def is_available(self):
        return True if self.quantity < self.item.inventory else False

    def minus_inventory(self):
        self.item.inventory -= self.quantity
        self.item.save()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    lineOrder = models.ManyToManyField(OrderDetail)
    shipping_price = models.IntegerField(null=True, blank=True, default=50000)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, null=True, blank=True)

    total = models.IntegerField(null=True, blank=True)
    ordered = models.BooleanField(default=False)

    @property
    def name(self):
        return "Testing"

    @property
    def netPaid(self):
        return self.total * 0.1

    def get_discount_price(self):
        discount = 0
        if self.coupon:
            print(self.coupon)
            discount = self.coupon.discount_value if self.coupon.discount_value else 0
        return discount

    def get_total_price(self):
        total = 0
        for order_item in self.lineOrder.all():
            total += order_item.get_total_item_price()
        return total

    def get_final_price(self):

        return self.get_total_price() + self.shipping_price + self.get_discount_price()
