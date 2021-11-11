from django.urls import path

import mainapp.views as mainapp
# from mainapp.views import product_add
app_name = 'mainapp'

urlpatterns = [
   path('', mainapp.ProductsListView.as_view(), name='product'),
   path('product_add/<int:product_id>/', mainapp.ProductsListView.as_view(), name='add_product'),
   # path('category_select/<int:category_id>/', mainapp.products, name='category_select'),
   path('category/<int:category_id>/', mainapp.ProductsListView.as_view(), name='category'),
   # path('page/<int:page>/<int:current_category>/', mainapp.ProductsListView.as_view(), name='page'),
   path('page/<int:page>/<int:current_category>/', mainapp.ProductsListView.as_view(), name='page'),
   path('detail/<int:pk>/', mainapp.ProductDetail.as_view(), name='detail'),
]