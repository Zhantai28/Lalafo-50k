# Generated by Django 3.2.6 on 2021-08-12 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('О', 'Одежда'), ('И', 'Игрушки'), ('Т', 'Транспорт'), ('У', 'Услуга'), ('М', 'Мебель'), ('Ж', 'Жилье'), ('ДЖ', 'Домашние животные'), ('ТЭ', 'Техника и электроника')], max_length=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category'),
        ),
    ]
