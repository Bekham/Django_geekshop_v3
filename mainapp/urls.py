from django.urls import path

import mainapp.views as mainapp
from mainapp.views import product_add
app_name = 'mainapp'

urlpatterns = [
   path('', mainapp.products, name='index'),
   path('product_add/<int:product_id>/<str:wtd>/', product_add, name='add_product'),
]