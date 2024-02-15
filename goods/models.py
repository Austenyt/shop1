from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from config import settings


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.CharField(max_length=150, verbose_name='Описание')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.CharField(max_length=150, verbose_name='Описание')
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    last_change_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='владелец')

    def current_version(self):
        return self.version_set.filter(is_current=True).first()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        permissions = [
            (
                'can_unpublish_product',
                'Can unpublish product',
            ),
            (
                'can_change_product_description',
                'Can change product description',
            ),
            (
                'can_change_product_category',
                'Can change product category',
            ),
        ]

    def assign_unpublish_permission(self, user):
        content_type = ContentType.objects.get_for_model(Product)
        permission = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=content_type,
            defaults={
                'name': 'Can unpublish product',
                'content_type': content_type,
            }
        )
        user.user_permissions.add(permission)

    def assign_change_product_description(self, user):
        content_type = ContentType.objects.get_for_model(Product)
        permission = Permission.objects.get(
            codename="can_change_product_description",
            content_type=content_type,
            defaults={
                'name': 'Can unpublish product',
                'content_type': content_type,
            }
        )
        user.user_permissions.add(permission)

    def assign_change_product_category(self, user):
        content_type = ContentType.objects.get_for_model(Product)
        permission = Permission.objects.get(
            codename="can_change_product_category",
            content_type=content_type,
            defaults={
                'name': 'Can change product description',
                'content_type': content_type,
            }
        )
        user.user_permissions.add(permission)


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_previews/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_name = models.CharField(max_length=250, verbose_name='Название версии')
    version_number = models.CharField(max_length=10, verbose_name='Номер версии', unique=True, blank=True, null=True)
    is_current = models.BooleanField(default=True, verbose_name='Актуальна')

    def __str__(self):
        return f'{self.product} - {self.version_name} - {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
