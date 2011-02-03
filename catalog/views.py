          # -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core import urlresolvers
from django.template import RequestContext
from catalog.models import Categories, Products
from catalog.forms import ProductAddToCartForm
from django.http import HttpResponseRedirect
from cart import cart

def index(request):
    # На главную отдаю только последние 3 тавара со спец ценой
    special_prices = Products.objects.filter(is_special_price=True)[0:3]
    # На главную отдаю только последние 3 тавара бестселлера
    bestsellers = Products.objects.filter(is_bestseller=True)[0:3]
    return render_to_response('main/index.html', locals(), context_instance=RequestContext(request))

def show_category(request, category_slug):
    category = get_object_or_404(Categories, slug=category_slug)
    products = category.products_set.filter(is_active=True)
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def show_product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    photos = product.productsphoto_set.all()
    features = product.features_set.all()
    page_title = str(product.brand) + ' ' + str(product.name)

    # evaluate the HTTP method, change as needed
    if request.method == 'POST':
        #create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        #check if posted data is valid
        if form.is_valid():
            #add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    else:
        #create the unbound form. Notice the request as a keyword argument
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set test cookie to make sure cookies are enabled
    request.session.set_test_cookie()
    return render_to_response("main/tovar.html", locals(), context_instance=RequestContext(request))

def about(request):
    return render_to_response('main/page.html', locals(), context_instance=RequestContext(request))

