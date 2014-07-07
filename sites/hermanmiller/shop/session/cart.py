# coding=utf-8


def _get_cart_data(request):
    return request.session.get('shop.cart', [])


def _get_order_data(request):
    return request.session.get('shop.order', {})


def get_data(request):
    cart_items = _get_cart_data(request)
    order = _get_order_data(request)
    return {'cart': cart_items, 'order': order}


def _set_cart_data(request, value):
    request.session['shop.cart'] = value


def _set_order_data(request, value):
    request.session['shop.order'] = value


def set_data(request, value):
    _set_cart_data(request, value['cart'])
    _set_order_data(request, value['order'])


def update_order_data(request, value):
    data = _get_order_data(request)
    data.update(value)
    _set_order_data(request, data)
    return data


def clear_cart_data(request):
    if 'shop.cart' in request.session:
        del request.session['shop.cart']


def clear_order_data(request):
    if 'shop.order' in request.session:
        del request.session['shop.order']
