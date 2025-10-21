from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='auth.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:home'), name='logout'),
    path('lk/', views.lk, name='lk'),
    path('order/', views.order, name='order'),
    path('card1/', views.card1, name='card1'),
    path('card2/', views.card2, name='card2'),
    path('card3/', views.card3, name='card3'),
]
