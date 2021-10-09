from django.urls import path
from baskets.views import basket_remove, basket_edit, basket_add
# import baskets.views as basket

app_name = 'baskets'

urlpatterns = [

    path('add/<int:product_id>/', basket_add, name='basket_add'),
    # path('add/<int:product_id>/', UserBasket.as_view(), name='basket_add'),
    path('remove/<int:product_id>/', basket_remove, name='basket_remove'),
    path('edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),

]