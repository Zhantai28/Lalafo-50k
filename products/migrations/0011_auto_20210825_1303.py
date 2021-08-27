# Generated by Django 3.2.6 on 2021-08-25 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('П', 'Продать'), ('К', 'Купить'), ('CА', 'Сдать в аренду'), ('А', 'Хочу арендовать')], max_length=3),
        ),
    ]