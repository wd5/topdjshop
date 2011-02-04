from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from catalog.forms import OrderForm
import cart

def show_cart(request, template_name="cart/cart.html"):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = OrderForm(postdata)

        if 'Remove' in postdata:
            cart.remove_from_cart(request)
        if 'Update' in postdata:
            cart.update_cart(request)
        if form.is_valid():
            cart.save_client(request, form)
            del request.session['cart_id']
            is_order = 1

    form = OrderForm()
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
