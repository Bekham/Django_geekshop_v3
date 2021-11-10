from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryAdminRegisterForm, \
    CategoryAdminProfileForm, ProductsAdminCreateForm, ProductsAdminProfileForm
from geekshop.mixin import CustomDispatchMixin
from mainapp.models import ProductCategory, Product
from users.models import User
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView


class AdminsListView(TemplateView):
    # title = 'GeekShop'
    template_name = 'admins/admin.html'

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #
    #     return context


# def index(request):
#     return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm

    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-read.html'
    success_url = reverse_lazy('admins:admins_user')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # self.object.is_active = False
        # self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    context_object_name = 'category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории товаров'
        return context


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    form_class = CategoryAdminRegisterForm
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание категории'
        return context


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = CategoryAdminProfileForm
    success_url = reverse_lazy('admins:admins_category')
    context_object_name = 'category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set. \
                    update(price=F('price') * (1 - discount / 100))

        return super().form_valid(form)

    @receiver(pre_save, sender=ProductCategory)
    def product_is_active_update_productcategory_save(sender, instance, **kwargs):
        if instance.pk:
            if instance.is_active:
                instance.product_set.update(is_active=True)
            else:
                instance.product_set.update(is_active=False)


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    success_url = reverse_lazy('admins:admins_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-read.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Продукты'
        context['categories'] = ProductCategory.objects.all()
        return context


class ProductsCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = ProductsAdminCreateForm
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание продукта'
        return context


class ProductsUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    form_class = ProductsAdminProfileForm
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class ProductsDeleteView(DeleteView):
    model = Product
    template_name = 'admins/admin-product-read.html'
    success_url = reverse_lazy('admins:admins_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # self.object.is_active = False
        # self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def db_profile_by_type(prefix, type, queries):
   update_queries = list(filter(lambda x: type in x['sql'], queries))
   print(f'db_profile {type} for {prefix}:')
   [print(query['sql']) for query in update_queries]
