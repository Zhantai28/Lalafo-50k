from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.enums import TextChoices
from django.db.models.fields import SlugField
from django.urls import reverse
from .managers import CategoryManager, SubategoryManager


class Category(models.Model):
    # objects = CategoryManager()
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=True, verbose_name="URL")
    # parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('product:product_list', args=[self.slug])

class Subcategory(models.Model):
    # objects = SubategoryManager()
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
    slug = models.SlugField(max_length=250, db_index=True, verbose_name="URL")
    description = models.TextField()
    price = models.CharField(max_length=255, default="Договорная")
    image = models.ImageField(blank=True, null=True, upload_to='products_photo')
    status = models.CharField(max_length=1, choices=(
        ("П", "Продать"),
        ("К", "Купить"),
    ))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name 
        
    # def get_absolute_url(self):
    #     return reverse('product:product_detail', args=[self.id, self.slug])

 
