from django.db import models
from django.db.models.enums import TextChoices
from django.db.models.fields import SlugField
from django.contrib.auth.models import  User 

class Category(models.Model):
    name = models.CharField(max_length=250,
    choices=(
        ("Одеж", "Oдежда"),
        ("Трант", "Транспорт"),
        ("Усл", "Услуги"),
        ("Игруш", "Игрушки"),
        ("Меб", "Мебель"),
        ("Элект", "Электроника"),

    ))
    slug = models.SlugField(max_length=250, unique=True, blank=True)



    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=250, db_index=True, blank=True)


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



class FeedBack(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name='Товары',
        related_name='product_comments'
    )

    text = models.TextField('Текст комментария')
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True,
        related_name="comment_child",
        on_delete=models.CASCADE
    )
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self): 
        return self.text, str(self.id)


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии' 
        ordering = ('created',)
