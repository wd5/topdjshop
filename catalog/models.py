          # -*- coding: utf-8 -*-
from django.db import models
from catalog.fields import ThumbnailImageField
from django.core.exceptions import ValidationError

class Brands(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Производитель'

class Sections(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Секции товара'

    def __unicode__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    section = models.ForeignKey(Sections)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Категории товара'

    @models.permalink
    def get_absolute_url(self):
        return ('catalog-page', [str(self.slug)])

def validate_even(value):
        if len(value) > 140:
            raise ValidationError(u'Количество символов: %s. Максимально разрешенное: 140'% len(value) )

class Products(models.Model):
    category = models.ForeignKey(Categories, verbose_name='Категория')
    brand = models.ForeignKey(Brands, verbose_name='Производитель')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Ссылка')
    price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name='Цена')
    mini_description = models.TextField(validators=[validate_even], help_text='Максимальное количество символов: 140.',
                                        verbose_name='Мини описание')
    html_description = models.TextField(blank=True, verbose_name='Описание', help_text='Описание в HTML')
    # Метаданные товара
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_bestseller = models.BooleanField(default=False, verbose_name='Лидер продаж')
    is_special_price = models.BooleanField(default=False, verbose_name='Специальная цена')
    is_discount = models.BooleanField(default=True, verbose_name='Скидка')
    # Временные отметки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product-page', [str(self.slug)])

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Товар'

class ProductsPhoto(models.Model):
    item = models.ForeignKey(Products)
    image = ThumbnailImageField(upload_to='products_image')

    class Meta:
        ordering = ['item']
        verbose_name_plural = 'Фото товара'

    def __unicode__(self):
        return self.item.name

    @models.permalink
    def get_absolute_url(self):
        return ('item_detail', None, {'object_id': self.id})

class FeaturesName(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Характеристики товара'

class Features(models.Model):
    name = models.ForeignKey(FeaturesName, verbose_name='Характеристика')
    value = models.CharField(max_length=50, verbose_name='Значение')
    item = models.ForeignKey(Products)
