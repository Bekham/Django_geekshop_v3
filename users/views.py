from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
# from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Create your views here.
from users.models import User


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Geekshop - Авторизация'
    # success_url = reverse_lazy('index')

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'GeekShop - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)
#


class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Geekshop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect(self.success_url)

        return redirect(reverse_lazy('users:register'))


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             if request.FILES:
#                 form.image = request.FILES['image']
#             form.save()
#             messages.success(request, 'Вы успешно зарагестрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': ' Geekshop - Регистрация',
#         'form': form,
#         'errors': form.errors
#
#     }
#     return render(request, 'users/register.html', context)


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop - Профайл'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user, )
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Изменения успешно сохранены!')
#             return HttpResponseRedirect(reverse('users:profile'))
#     context = {
#         'title': 'Geekshop-Профайл',
#         'form': UserProfileForm(instance=request.user),
#         'baskets': Basket.objects.filter(user=request.user)
#     }
#     return render(request, 'users/profile.html', context)


class Logout(LogoutView):
    template_name = 'mainapp/index.html'
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
