from django.conf import settings
from django.db import models


class Customer(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, null=True, blank=True)
    client_ip = models.CharField(max_length=1000, null=True, blank=True)
