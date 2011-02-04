from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.forms import OrderForm
from django.core.mail import send_mail
import cart
import threading

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
            t = threading.Thread(target=send_mail('Subject here', 'Here is the message.', 'freebsdstuff@gmail.com', ['freebsdstuff@gmail.com'], fail_silently=False))
            t.setDaemon(True)
            t.start()
    else:
        form = OrderForm()

    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
