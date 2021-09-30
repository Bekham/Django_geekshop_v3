from django.shortcuts import render
import os
import json
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
from users.models import User

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

    db_products_download = False
    if db_products_download:
        file_path = os.path.join(MODULE_DIR, 'fixtures/products_content.json')
        products_content = json.load(open(file_path, encoding='utf-8'))
        for product in products_content:
            add_product = Product(name=product['name'],
                                  image=product['image'],
                                  description=product['description'],
                                  price=product['price'],
                                  quantity=10,
                                  category_id=int(product['category']))
            add_product.save()

    context = {
        'title': 'GeekShop - Каталог',
        'now_date': False,
        'products': Product.objects.all(),



    }
    return render(request, 'mainapp/products.html', context)
