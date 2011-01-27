          # -*- coding: utf-8 -*-
from django.db import models
from catalog.fields import ThumbnailImageField


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    # Производитель
    brand = models.ForeignKey('catalog.Brand')
    # Метаданные товара
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_special_price = models.BooleanField(default=False)
    # Временные отметки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class HeadphonesCategory(Category):
    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = 'Категории наушников'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog-page', [str(self.slug)])

class Headphones(Product):
    category = models.ForeignKey(HeadphonesCategory, verbose_name='category_id')
    Type = models.CharField(max_length=50, help_text="Тип подключения. например проводные")
    Length = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, help_text="Длина провода")
    Features = models.CharField(max_length=200, blank=True, null=True, help_text="Особенности")
    Connector = models.CharField(max_length=200, help_text="Разъем подключения. например mini jack 3.5 mm")
    html_description = models.TextField()
    mini_description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('product-page', [str(self.slug)])

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def get_features(self):
        return [self.Type, self.Length, self.Features, self.Connector]

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Наушники'

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Производитель'

class HeadPhonesPhoto(models.Model):
    item = models.ForeignKey(Headphones)
    title = models.CharField(max_length=100)
    image = ThumbnailImageField(upload_to='images/products')
#    image = StdImageField(upload_to='images/products', blank=True, size=(300, 220), thumbnail_size=(196, 200, True))
    caption = models.CharField(max_length=250, blank = True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Фото наушников'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('item_detail', None, {'object_id': self.id})
