from django.db import models
from django.contrib.auth.models import  User
# from django.db.models.fields.files import ImageField 
from django.contrib.postgres.fields import ArrayField 
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
        return reverse('account:product_by_category',
                        args=[self.id])
  


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=255, default="Договорная")
    image = models.ImageField(blank = True, upload_to='products_photo')
    status = models.CharField(max_length=3, choices=(
        ("П", "Продать"),
        ("К", "Купить"),
        ("CA", "Сдать в аренду"),
        ("А", "Хочу арендовать")
    ))
    city = models.CharField(max_length=255)
    active = models.BooleanField(default=True,  verbose_name='Активный')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        null=True,
        related_name='creator'

    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name 

           
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id])

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def get_product(self):
        return Product.objects.filter(category__name=self.name)



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

    text = models.TextField('Текст отзыва')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self): 
        return self.text[0:220]


    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии' 
        ordering = ('created',)




# КОРЗИНА



  
class Cart(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE, related_name='carts')
           
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
