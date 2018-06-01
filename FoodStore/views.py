import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from FoodStore.models import Cart, Item


@csrf_exempt
def get_items(request):
    response_data = {
        'items': []
    }

    for item in Item.objects.all():
        item = {
            'id': item.id,
            'name': item.title,
            'price': item.price,
            'weight': item.weight,
            'description': item.description,
        }
        response_data['items'].append(item)

    return JsonResponse(response_data, content_type='application/json')


@csrf_exempt
def add_item_to_cart(request):
    body = json.loads(request.body)
    request_cart_id = body['cart_id']
    request_item_id = body['item_id']

    cart_id = get_current_session_cart_id(cart_id=request_cart_id)
    cart = Cart.objects.get(pk=cart_id)

    cart.upsert_item(item_id=request_item_id)

    response_data = cart_to_json(cart=cart)

    return JsonResponse(response_data, content_type='application/json')


@csrf_exempt
def remove_item_from_cart(request):
    body = json.loads(request.body)
    request_cart_id = body['cart_id']
    request_item_id = body['item_id']

    cart_id = get_current_session_cart_id(cart_id=request_cart_id)
    cart = Cart.objects.get(pk=cart_id)

    cart.remove_item(item_id=request_item_id)

    response_data = cart_to_json(cart=cart)

    return JsonResponse(response_data, content_type='application/json')


def get_current_session_cart_id(cart_id):
    try:
        cart = Cart.objects.get(pk=cart_id)
    except:
        cart = None

    if cart is None:
        cart = Cart()
        cart.save()

    return cart.id


def cart_to_json(cart):
    response_data = {
        'cart_id': cart.id,
        'price': cart.get_price(),
        'items': []
    }

    for cart_item in cart.items.all():
        item = {
            'item_id': cart_item.item.id,
            'quantity': cart_item.quantity,
            'name': cart_item.item.title,
            'description': cart_item.item.description,
            'price': cart_item.get_price()
        }
        response_data['items'].append(item)

    return response_data
