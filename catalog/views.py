          # -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from catalog.models import HeadphonesCategory, Headphones

def index(request):
    active_categories = HeadphonesCategory.objects.filter(is_active=True)
    return render_to_response('main/index2.html', locals(), context_instance=RequestContext(request))

def show_category(request, category_slug):
    c = get_object_or_404(HeadphonesCategory, slug=category_slug)
    products = c.headphones_set.all()
    return render_to_response('catalog.html', locals(), context_instance=RequestContext(request))

def show_product(request, product_slug):
    c = get_object_or_404(Headphones, slug=product_slug)
    photos = c.headphonesphoto_set.all()
    try:
        photo = photos[0]
    except :
        pass
    product_category = c.category.name
    features = c.get_features()
    ttt = ["1","2"]
    return render_to_response('tovar.html', locals(), context_instance=RequestContext(request))
