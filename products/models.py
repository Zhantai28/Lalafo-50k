from django.db import models
from django.db.models.enums import TextChoices
from django.db.models.fields import SlugField
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, unique=True, verbose_name="URL")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, verbose_name="URL")
    description = models.TextField()
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=12)
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
        
    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.id, self.slug])

