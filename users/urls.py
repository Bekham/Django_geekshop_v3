from django.urls import path
from users.views import LoginListView, RegisterListView, ProfileFormView, Logout, verify

app_name = 'users'

urlpatterns = [
   path('login/', LoginListView.as_view(), name='login'),
   path('register/', RegisterListView.as_view(), name='register'),
   path('profile/', ProfileFormView.as_view(), name='profile'),
   path('logout/', Logout.as_view(), name='logout'),
   path('verify/<str:email>/<str:activation_key>/',verify,name='verify')
]
