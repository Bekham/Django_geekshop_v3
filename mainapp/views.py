from django.http import JsonResponse
from django.shortcuts import render
import os
import json
from django.template.loader import render_to_string
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from baskets.views import basket_add, basket_remove
from baskets.models import Basket

# Create your views here.


MODULE_DIR = os.path.dirname(__file__)


def index(request):
    context = {
        'title': 'GeekShop',
        'head': 'GeekShop Store',
        'now_date': True,
        # 'user': User.username,

    }
    return render(request, 'mainapp/index.html', context)


@login_required
def products(request):
    _products = Product.objects.all()

    context = {
        'title': 'GeekShop - Каталог',
        'now_date': False,
        'products': _products,
        'baskets': Basket.objects.filter(user=request.user).values('product_id'),
    }
    print(context['baskets'])
    return render(request, 'mainapp/products.html', context)


@login_required
def product_add(request, product_id, wtd):
    if request.is_ajax():
        if wtd == 'Отправить в корзину':
            basket_add(request, product_id=product_id)
        elif wtd == 'Удалить из корзины':
            # basket_add(request, product_id=product_id)
            basket_remove(request, product_id=product_id)
        context = {
            'title': 'GeekShop - Каталог',
            'products': Product.objects.all(),
            'baskets': Basket.objects.filter(user=request.user).values('product_id'),
        }

        result = render_to_string('mainapp/goods.html', context)
        return JsonResponse({'result': result})


