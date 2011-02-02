          # -*- coding: utf-8 -*-
from django.db import models
from catalog.fields import ThumbnailImageField

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

    def __unicode__(self):
        return self.name

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

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Категории товара'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('catalog-page', [str(self.slug)])

class Products(models.Model):
    category = models.ForeignKey(Categories, verbose_name='category_id')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=9,decimal_places=2)
    # Производитель
    brand = models.ForeignKey(Brands)
    # Метаданные товара
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_special_price = models.BooleanField(default=False)
#    is_discount = models.BooleanField(default=True)
    # Временные отметки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    html_description = models.TextField()
    mini_description = models.CharField(max_length=140)

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
    title = models.CharField(max_length=100)
    image = ThumbnailImageField(upload_to='products_image')
    caption = models.CharField(max_length=250, blank = True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Фото товара'

    def __unicode__(self):
        return self.title

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
    name = models.ForeignKey(FeaturesName)
    value = models.CharField(max_length=50)
    item = models.ForeignKey(Products)
