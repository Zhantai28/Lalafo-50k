from django.db import models
from django.contrib.auth.models import  User 
from account.models import Profile
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Category', kwargs={'id': self.id, 'name': self.name})


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=255, default="Договорная")
    image = models.ImageField(blank=True, null=True, default='default.jpg', upload_to='products_photo')
    status = models.CharField(max_length=3, choices=(
        ("П", "Продать"),
        ("К", "Купить"),
        ("CA", "Сдать в аренду"),
        ("А", "Хочу арендовать")
    ))
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_profile = models.ForeignKey(
        to=User, 
        on_delete=models.SET_NULL, 
        null=True
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name 
        
    def get_absolute_url(self):
        return reverse('product', kwargs=(str(self.id),))



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