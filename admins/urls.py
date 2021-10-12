from django.urls import path
from admins.views import UserListView, UserUpdateView, UserCreateView, UserDeleteView, CategoryListView, \
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ProductsListView, AdminsListView, ProductsCreateView, \
    ProductsUpdateView, ProductsDeleteView

# import baskets.views as basket

app_name = 'admins'

urlpatterns = [
    path('', AdminsListView.as_view(), name='admin'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
    path('category/', CategoryListView.as_view(), name='admins_category'),
    path('category-create/', CategoryCreateView.as_view(), name='admins_category_create'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='admins_category_update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='admins_category_delete'),
    path('products/', ProductsListView.as_view(), name='admins_products'),
    path('products-create/', ProductsCreateView.as_view(), name='admins_products_create'),
    path('products-update/<int:pk>/', ProductsUpdateView.as_view(), name='admins_products_update'),
    path('products-delete/<int:pk>/', ProductsDeleteView.as_view(), name='admins_products_delete'),
]
