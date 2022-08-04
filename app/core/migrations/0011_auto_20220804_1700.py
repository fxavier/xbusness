# Generated by Django 3.2.15 on 2022-08-04 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_alter_product_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.TextField()),
                ('rate', models.IntegerField(default=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='sale_price_old',
            new_name='sales_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sale_price_new',
        ),
        migrations.AddField(
            model_name='product',
            name='numReviews',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.DeleteModel(
            name='ProductComment',
        ),
        migrations.AddField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_comments', to='core.product'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
