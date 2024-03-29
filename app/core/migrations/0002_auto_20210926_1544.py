# Generated by Django 3.2.7 on 2021-09-26 15:44

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sale',
            new_name='discount',
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price_new',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=16, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price_old',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=16, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.CharField(blank=True, choices=[('Novo', 'Novo'), ('Usado', 'Usado')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.CharField(blank=True, choices=[('Oferta do dia', 'Oferta do dia'), ('Quente', 'Quente'), ('Mais vendido', 'Mais Vendido')], max_length=100, null=True),
        ),
    ]
