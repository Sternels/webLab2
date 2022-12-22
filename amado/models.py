from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image_one = models.ImageField(upload_to='static/product/')
    image_two = models.ImageField(upload_to='static/product/')
    image_three = models.ImageField(upload_to='static/product/')
    image_four = models.ImageField(upload_to='static/product/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Cart(models.Model):
    guest_session_id = models.CharField(max_length=200)
    date_create = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f'{self.guest_session_id} - {self.date_create}'


class CartDetails(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    count = models.IntegerField()

    class Meta:
        verbose_name = 'Элемент деталей корзины'
        verbose_name_plural = 'Детали корзины'

    def __str__(self):
        return f'{self.cart_id} - {self.product.name}'


class Status(models.Model):
    name = models.CharField(max_length=50)


class Orders(models.Model):
    guest_session_id = models.CharField(max_length=200, verbose_name='ИД сессии гостя')
    fname = models.CharField(max_length=200, verbose_name='Имя')
    lname = models.CharField(max_length=200, verbose_name='Фамилия')
    mail = models.CharField(max_length=200, verbose_name='Почта')
    date_create = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')
    zip = models.CharField(max_length=200, null=True, verbose_name='Почтовый индекс')
    comment = models.CharField(max_length=400, null=True, verbose_name='Комментарий')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, verbose_name='Статус')
    total_sum = models.DecimalField(null=True, max_digits=20, decimal_places=2, verbose_name='Итоговая сумма')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.guest_session_id} - {self.date_create} - {self.status}'


class OrderDetails(models.Model):
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE, verbose_name='ИД заказа')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент деталей заказа'
        verbose_name_plural = 'Детали заказов'

    def __str__(self):
        return f'{self.product.name} - {self.product.price}р'
