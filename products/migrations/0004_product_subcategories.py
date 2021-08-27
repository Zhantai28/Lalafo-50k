# Generated by Django 3.2.6 on 2021-08-20 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_subcategories'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategorys', to='products.subcategory', verbose_name='Подкатегория'),
        ),
    ]