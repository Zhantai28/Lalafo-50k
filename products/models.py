from django.db import models
from account.models import Profile
from django.urls import reverse

class Node(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('', kwargs={'id': self.id, 'name': self.name})


class Subcategory(models.Model):
    name = models.CharField('Название подкатегории', max_length=250)
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    categories = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Subcategory, related_name='subcategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, db_index=True)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=255, default="Договорная")
    image = models.ImageField(blank=True, null=True, upload_to='products_photo')
    status = models.CharField(max_length=3, choices=(
        ("П", "Продать"),
        ("К", "Купить"),
        ("CА", "Сдать в аренду"),
        ("А", "Хочу арендовать")
    ))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_profile = models.ForeignKey(
        to=Profile, 
        on_delete=models.SET_NULL, 
        null=True
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name 
        
    def get_absolute_url(self):
        return reverse('product', args=[str (self.id)])

 
