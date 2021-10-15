import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
# from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from geekshop.mixin import UserDispatchMixin
from mainapp.models import Product
from baskets.models import Basket


# Create your views here.

class UserBasketCreateView(CreateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'mainapp/products.html'
    success_url = reverse_lazy('products:index')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'product_id' in kwargs:
            fromAjax = request.POST['page_id']
            # products_list = fromAjax[1:-1].split(', ')
            # page_products = {}
            # # fromJs = fromJs.encode('utf-8')
            # for item in products_list:
            #     page_products_item = Product.objects.find(name=item[9:-9])
            #
            #     print(page_products_item)

            # now we can load our JSON from JS
            # fromJs = json.loads(fromAjax)[0]
            # products = request.POST.get('page_id')
            # print(fromJs)
            # for i in products:
            #     print(i)
            product_id = self.kwargs.get('product_id')
            if product_id:
                product = Product.objects.get(id=product_id)
                baskets = Basket.objects.filter(user=request.user, product=product)
                # if request.is_ajax():
                if baskets.exists():
                    basket = baskets.first()
                    basket.quantity += 1
                    basket.save()
                else:
                    Basket.objects.create(user=request.user, product=product, quantity=1)
            context = {
                'products': Product.objects.all()
            }
                    # print(context)
                    # update['new_baskets'] = Basket.objects.filter(user=request.user)
            result = render_to_string('include/goods.html', context, request=request)
            return JsonResponse({'result': result})


class UserBasketDeleteView (DeleteView, UserDispatchMixin):
    model = Basket
    success_url = reverse_lazy('users:profile')


class UserBasketUpdateView (UpdateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    pk_url_kwarg = 'basket_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserBasketUpdateView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        super(UserBasketUpdateView, self).get(request, *args, **kwargs)
        if request.is_ajax():
            basket_id = self.kwargs.get(self.pk_url_kwarg)
            quantity = self.kwargs.get('quantity')
            baskets = Basket.objects.filter(id=basket_id)
            if baskets.exists():
                basket = baskets.first()
                if quantity > 0:
                    basket.quantity = quantity
                    basket.save()
                else:
                    basket.delete()
            result = render_to_string('baskets/baskets.html', self.get_context_data(**kwargs), request=request)
            return JsonResponse({'result': result})
        return redirect(self.success_url)

#

# @login_required
# def basket_add(request, product_id):
#     user_select = request.user
#     product = Product.objects.get(id=product_id)
#     baskets = Basket.objects.filter(user=user_select, product=product)
#     if not baskets.exists():
#         Basket.objects.create(user=user_select, product=product, quantity=1)
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required
# def basket_remove(request, product_id):
#     Basket.objects.get(id=product_id).delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#

# @login_required
# def basket_edit(request, id, quantity):
#     if request.is_ajax():
#         basket = Basket.objects.get(id=id)
#         if quantity > 0:
#             basket.quantity = quantity
#             basket.save()
#         else:
#             basket.delete()
#         # baskets = Basket.objects.filter(user=request.user)
#         # context = {
#         #     'baskets': baskets,
#         # }
#         # result = render_to_string('baskets/baskets.html', context)
#         result = render_to_string('baskets/baskets.html', request=request)
#         return JsonResponse({'result': result})

