from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomAuthenticationForm


app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='auth.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('lk/', views.lk, name='lk'),
    path('order/', views.order, name='order'),
    path('card/', views.card, name='card'),
]
