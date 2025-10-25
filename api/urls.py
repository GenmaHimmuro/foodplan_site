from django.urls import path

from .views import CreateOrderView, PromoValidateView


urlpatterns = [
    path('order/', CreateOrderView.as_view(), name='api_order_create'),
    path('promo/validate/', PromoValidateView.as_view(), name='api_promo_validate'),
]

