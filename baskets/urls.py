from django.urls import path
from baskets.views import UserBasketCreateView, UserBasketDeleteView, UserBasketUpdateView

# import baskets.views as basket

app_name = 'baskets'

urlpatterns = [

    path('add/<int:product_id>/', UserBasketCreateView.as_view(), name='basket'),
    # path('add/<int:product_id>/', UserBasket.as_view(), name='basket_add'),
    path('remove/<int:pk>/', UserBasketDeleteView.as_view(), name='basket_remove'),
    path('edit/<int:basket_id>/<int:quantity>/', UserBasketUpdateView.as_view(), name='basket_edit'),

]