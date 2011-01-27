          # -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from catalog.models import Categories, Products

def index(request):
    # На главную отдаю только последние 3 тавара со спец ценой
    special_prices = Products.objects.filter(is_special_price=True)[0:3]
    # На главную отдаю только последние 3 тавара бестселлера
    bestsellers = Products.objects.filter(is_bestseller=True)[0:3]
    return render_to_response('main/index.html', locals(), context_instance=RequestContext(request))

def show_category(request, category_slug):
    category = get_object_or_404(Categories, slug=category_slug)
    products = category.products_set.all()
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def show_product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    photos = product.productsphoto_set.all()
    try:
        photo = photos[0]
    except :
        pass
    product_category = product.category.name
    features = product.features_set.all()
#    features = product.get_features()
    return render_to_response("main/tovar.html", locals(), context_instance=RequestContext(request))
