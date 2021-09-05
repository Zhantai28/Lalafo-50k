from django.db import models
from django.db.models.enums import TextChoices

from django.contrib.auth.models import  User 
import account.models  
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
    # slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
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
        to='account.Profile', 
        on_delete=models.SET_NULL, 
        null=True
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name 
        
    def get_absolute_url(self):
        return reverse('product', args=[str (self.id)])



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
    image = models.ImageField(upload_to='products', null=True, blank=True)

    def __str__(self): 
        return self.text, str(self.id)


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии' 
        ordering = ('created',)





# кОРЗИНА



  
class Cart(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey('account.Profile', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
 
    
           
    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

class CartItem(models.Model):
    cart= models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.name

# p = Product
# p_is_ordered = CartItem.objects.filter(cart__owner=user, product=p).exists()