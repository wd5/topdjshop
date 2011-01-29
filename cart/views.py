from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from catalog.forms import OrderForm
import cart

def show_cart(request, template_name="cart/cart.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = OrderForm(postdata)

        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Good':
            return HttpResponseRedirect('/')
        if form.is_valid():
            cart.save_client(request)
            del request.session['cart_id']
            is_order = 1

    form = OrderForm()
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
