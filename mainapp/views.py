from django.http import JsonResponse
from django.shortcuts import render
import os
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from geekshop.mixin import UserDispatchMixin
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from baskets.views import basket_add
from baskets.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


MODULE_DIR = os.path.dirname(__file__)


class IndexView(TemplateView):
    title = 'GeekShop'
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['head'] = 'GeekShop Store'
        return context


# def index(request):
#     context = {
#         'title': 'GeekShop',
#         'head': 'GeekShop Store',
#     }
#     return render(request, 'mainapp/index.html', context)


class ProductsListView(UserDispatchMixin, ListView):
    model = Product
    template_name = 'mainapp/products.html'
    title = 'GeekShop - Каталог'

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        request = self.request
        product_all = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        current_category = self.kwargs.get('current_category')
        page = self.kwargs.get('page')
        if category_id or current_category:
            if category_id:
                current_category = category_id
            products = product_all.filter(category_id=current_category)
        else:
            products = product_all
            current_category = 0
        paginator = Paginator(products, per_page=3)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context['object_list'] = products_paginator
        context['categories'] = ProductCategory.objects.all()
        context['baskets_product_id'] = Basket.objects.filter(user=request.user)
        context['current_category'] = current_category
        wtd = self.kwargs.get('wtd')
        product_id = self.kwargs.get('product_id')
        if request.is_ajax():
            if wtd == 'Отправить в корзину':
                basket_add(request, product_id=product_id)
            elif wtd == 'Удалить из корзины':
                Basket.objects.filter(product_id=product_id).filter(user_id=request.user).delete()
            context['baskets_product_id'] = Basket.objects.filter(user=request.user)
        return context

    def render_to_response(self, context, **response_kwargs):
        """ Allow AJAX requests to be handled more gracefully """
        if self.request.is_ajax():
            print(context['baskets_product_id'])
            result = render_to_string('mainapp/goods.html', context)
            return JsonResponse({'result': result})
        else:
            return super(ProductsListView, self).render_to_response(context, **response_kwargs)


# @login_required
# def products(request, category_id=None, page_id=1, product_id=None, wtd=None, current_category=0):
#
#     if category_id is not None:
#         _products = Product.objects.filter(category_id=category_id)
#         if current_category != 0:
#             current_category = current_category
#         else:
#             current_category = category_id
#     elif current_category != 0:
#         _products = Product.objects.filter(category_id=current_category)
#     else:
#         _products = Product.objects.all()
#     print('end', current_category, page_id, category_id)
#     paginator = Paginator(_products, per_page=2)
#     try:
#         products_paginator = paginator.page(page_id)
#     except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#     except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)
#     context = {
#         'title': 'GeekShop - Каталог',
#         'now_date': False,
#         'products': products_paginator,
#         'baskets': Basket.objects.filter(user=request.user).values('product_id'),
#         'categories': ProductCategory.objects.all(),
#         'current_category': current_category,
#     }
#     if request.is_ajax():
#         if wtd is not None:
#             if wtd == 'Отправить в корзину':
#                 basket_add(request, product_id=product_id)
#             elif wtd == 'Удалить из корзины':
#                 Basket.objects.filter(product_id=product_id).filter(user_id=request.user).delete()
#             result = render_to_string('mainapp/goods.html', context)
#             return JsonResponse({'result': result})
#         # if category_id is not None:
#         #     result = render_to_string('mainapp/category.html', context)
#         #     return JsonResponse({'result': result})
#     else:
#         return render(request, 'mainapp/products.html', context)


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


