from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from subscription.forms import OrderForm
from subscription.models import Subscription, Promotion
from foodplan_site.models import Allergen, DietInfo
from django.db.utils import OperationalError, ProgrammingError
from datetime import date


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('accounts:order')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})


def home(request):
    return render(request, 'index.html')


@login_required
def lk(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        user = request.user
        if name:
            user.name = name
        if password and password == password_confirm:
            user.password = make_password(password)
        elif password and password != password_confirm:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'lk.html', {'user': user})

        user.save()
        messages.success(request, 'Данные успешно обновлены!')
        return redirect('accounts:lk')

    context = {'user': request.user}
    try:
        active_subscriptions = (
            request.user.subscriptions.filter(expiring_date__gte=date.today())
            .order_by('-start_date')
        )
        diet_map = {d.code: d for d in DietInfo.objects.all()}
        for s in active_subscriptions:
            s.meals_count = int(s.is_breakfast) + int(s.is_lunch) + int(s.is_dinner) + int(s.is_dessert)
            diet = diet_map.get(s.diet_type)
            s.diet_description = getattr(diet, 'description', '') if diet else ''
        context['active_subscriptions'] = active_subscriptions
    except (OperationalError, ProgrammingError):
        context['active_subscriptions'] = []
    return render(request, 'lk.html', context)


@login_required
def order(request):
    context = {}
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            promotion = None
            promo_code = form.cleaned_data.get('promo_code')
            if promo_code:
                promotion = Promotion.objects.filter(discount_code=promo_code.strip(), is_active=True).first()
                if not promotion:
                    messages.error(request, 'Промокод не найден или не активен. Скидка не применена.')

            subscription = Subscription(
                user=request.user,
                duration=form.cleaned_data['duration'],
                diet_type=form.cleaned_data['diet_type'],
                is_breakfast=form.cleaned_data['is_breakfast'],
                is_lunch=form.cleaned_data['is_lunch'],
                is_dinner=form.cleaned_data['is_dinner'],
                is_dessert=form.cleaned_data['is_dessert'],
                persons=form.cleaned_data.get('persons', 1),
                promotion=promotion,
            )
            subscription.save()
            allergens_qs = form.cleaned_data.get('excluded_allergens')
            if allergens_qs:
                subscription.excluded_allergens.set(allergens_qs)

            messages.success(request, f'Подписка создана. Стоимость: {subscription.price}₽')
            context.update({'price': subscription.price, 'applied_promo': bool(promotion)})
        else:
            context['form_errors'] = form.errors
        context['form'] = form
    else:
        context['form'] = OrderForm()

    try:
        context['allergens'] = Allergen.objects.all()
    except (OperationalError, ProgrammingError):
        context['allergens'] = []
    return render(request, 'order.html', context)


def card(request):
    return render(request, 'card.html')
