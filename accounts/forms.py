from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов.')
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        if commit:
            user.save()
        return user
    

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Неверный email или пароль. "
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['password'].label = 'Пароль'

    class Meta:
        fields = ['username', 'password']
