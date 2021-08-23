# Generated by Django 3.2.6 on 2021-08-20 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250)),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='URL')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название подкатегории')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('categories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250)),
                ('slug', models.SlugField(max_length=250, verbose_name='URL')),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, default='Договорная', max_digits=12)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products_photo')),
                ('status', models.CharField(choices=[('П', 'Продать'), ('К', 'Купить')], max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.category')),
                ('subcategories', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategorys', to='products.subcategory', verbose_name='Подкатегория')),
            ],
            options={
                'ordering': ('name',),
                'index_together': {('id', 'slug')},
            },
        ),
    ]
