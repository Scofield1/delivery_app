from .models import *
import json


def cookiesCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        print(cart)
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_items_total': 0}
    cartitems = order['get_items_total']

    for index in cart:
        try:
            cartitems += cart[index]['quantity']

            product = Product.objects.get(id=index)
            total = (product.price * cart[index]['quantity'])
            order['get_cart_total'] += total
            order['get_items_total'] += cart[index]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity': cart[index]['quantity'],
                'get_total': total
            }
            items.append(item)
        except:
            pass

    return {'items': items, 'order': order, 'cartitems': cartitems}


def cartData(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.order_items.all()
        cartitems = order.get_items_total
    else:
        cookiesData = cookiesCart(request)
        cartitems = cookiesData['cartitems']
        order = cookiesData['order']
        items = cookiesData['items']
    return {'items': items, 'order': order, 'cartitems': cartitems}