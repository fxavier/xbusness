# Generated by Django 3.2.15 on 2022-08-04 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20220804_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
