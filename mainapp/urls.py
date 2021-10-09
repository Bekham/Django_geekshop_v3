from django.urls import path

import mainapp.views as mainapp
# from mainapp.views import product_add
app_name = 'mainapp'

urlpatterns = [
   path('', mainapp.products, name='index'),
   path('product_add/<int:product_id>/<str:wtd>/', mainapp.products, name='add_product'),
   # path('category_select/<int:category_id>/', mainapp.products, name='category_select'),
   path('category/<int:category_id>/', mainapp.products, name='category'),
   path('page/<int:page_id>/<int:current_category>/', mainapp.products, name='page'),
]