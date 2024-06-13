from django.db import models

from users.models import User, NULLABLE


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    desc = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    desc = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.SET_NULL, **NULLABLE)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2, verbose_name='цена за шт.')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата изменения')
    is_published = models.BooleanField(default=True, verbose_name="опубликован")
    author = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Автор')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)

        permissions = [
            (
                'set_published',
                'Can change is_published field'
            ),
            (
                'change_category',
                'Can change category'
            )
        ]


class Contact(models.Model):
    country = models.CharField(max_length=50, verbose_name='страна')
    phone = models.CharField(default='test', max_length=16)
    address = models.CharField(max_length=100, verbose_name='Почтовый адрес')

    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'контактная информация'
        verbose_name_plural = verbose_name
        ordering = ('phone',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='version', verbose_name='продукт')
    name = models.CharField(max_length=100, verbose_name='название версии')
    num = models.IntegerField(default=0, verbose_name='номер версии')
    is_active = models.BooleanField(default=True, verbose_name='актуальность')

    def __str__(self):
        return f'{self.is_active}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
