from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from datetime import date
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения'
    )
    phone = forms.CharField(
        max_length=20,
        label='Номер телефона',
        help_text='Формат: +375 (29) XXX-XX-XX'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'birth_date', 'password1', 'password2')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError('Вы должны быть старше 18 лет для регистрации')
        return birth_date


