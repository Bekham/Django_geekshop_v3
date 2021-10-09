from django.http import JsonResponse
from django.shortcuts import render
import os
from django.template.loader import render_to_string
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from baskets.views import basket_add
from baskets.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


MODULE_DIR = os.path.dirname(__file__)


def index(request):
    context = {
        'title': 'GeekShop',
        'head': 'GeekShop Store',
        'now_date': True,

    }
    return render(request, 'mainapp/index.html', context)


@login_required
def products(request, category_id=None, page_id=1, product_id=None, wtd=None, current_category=0):
    print(current_category, page_id, category_id)
    if category_id is not None:
        _products = Product.objects.filter(category_id=category_id)
        if current_category != 0:
            current_category = current_category
        else:
            current_category = category_id
    elif current_category != 0:
        _products = Product.objects.filter(category_id=current_category)
    else:
        _products = Product.objects.all()
    print('end', current_category, page_id, category_id)
    paginator = Paginator(_products, per_page=2)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context = {
        'title': 'GeekShop - Каталог',
        'now_date': False,
        'products': products_paginator,
        'baskets': Basket.objects.filter(user=request.user).values('product_id'),
        'categories': ProductCategory.objects.all(),
        'current_category': current_category,
    }
    if request.is_ajax():
        if wtd is not None:
            if wtd == 'Отправить в корзину':
                basket_add(request, product_id=product_id)
            elif wtd == 'Удалить из корзины':
                Basket.objects.filter(product_id=product_id).filter(user_id=request.user).delete()
            result = render_to_string('mainapp/goods.html', context)
            return JsonResponse({'result': result})
        # if category_id is not None:
        #     result = render_to_string('mainapp/category.html', context)
        #     return JsonResponse({'result': result})
    else:
        return render(request, 'mainapp/products.html', context)


# @login_required
# def product_add(request, product_id, wtd):
#     if request.is_ajax():
#         if wtd == 'Отправить в корзину':
#             basket_add(request, product_id=product_id)
#         elif wtd == 'Удалить из корзины':
#             Basket.objects.filter(product_id=product_id).filter(user_id=request.user).delete()
#         context = {
#             'title': 'GeekShop - Каталог',
#             'products': Product.objects.all(),
#             'baskets': Basket.objects.filter(user=request.user).values('product_id'),
#         }
#         result = render_to_string('mainapp/goods.html', context)
#         return JsonResponse({'result': result})


