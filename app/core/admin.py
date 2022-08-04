from django.contrib import admin
from core.models.customer import Customer
from core.models.person import Person, Phone, Bank
from core.models.product import Product, Category, Brand, Unity, ImageUpload, ProductImage
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
    Unity,
    Provider,
    Transporter,
    Vehicle,
    ImageUpload,
    ProductImage
]

for model in classes:
    admin.site.register(model)
