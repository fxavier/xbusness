from django.contrib import admin
from core.models.customer import Customer
from core.models.person import Person, Phone, Bank
from core.models.product import Product, Category, Brand, Coupon, Unity
from core.models.provider import Provider
from core.models.transporter import Transporter, Vehicle

classes = [
    Customer,
    Person,
    Phone,
    Bank,
    Product,
    Category,
    Brand,
    Coupon,
    Unity,
    Provider,
    Transporter,
    Vehicle
]

for model in classes:
    admin.site.register(model)
