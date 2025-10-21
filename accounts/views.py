from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LogoutView


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('accounts:home')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})


def home(request):
    return render(request, 'index.html')


def lk(request):
    return render(request, 'lk.html')


def order(request):
    return render(request, 'order.html')


def card1(request):
    return render(request, 'card1.html')


def card2(request):
    return render(request, 'card2.html')


def card3(request):
    return render(request, 'card3.html')
