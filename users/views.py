from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
# from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm

# Create your views here.
from users.models import User, UserProfile


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
            user = form.save()
            if send_verify_link(user):
                messages.success(request, 'Вы успешно зарегистрировались')
            return redirect(self.success_url)
        print(form.error_messages)
        # print(form.password1)
        # print(form.password2)
        return render(request, 'users/register.html', {'form': form})
        # return redirect(self.success_url)


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
        # context['baskets'] = Basket.objects.filter(user=self.request.user)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
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


def send_verify_link(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
    message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user)
        return render(request, 'users/verification.html')
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))
