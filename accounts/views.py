from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password


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

    return render(request, 'lk.html', {'user': request.user})


def order(request):
    return render(request, 'order.html')


def card1(request):
    return render(request, 'card1.html')


def card2(request):
    return render(request, 'card2.html')


def card3(request):
    return render(request, 'card3.html')
