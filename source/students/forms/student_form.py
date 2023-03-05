from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import DateInput, TextInput
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from accounts.models import Account

from applications.models import StudentSex


class StudentForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label=_('Подтвердите пароль'), strip=False, required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(choices=StudentSex.choices,
                            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': _('Пол')}))
    phone_number = PhoneNumberField(region='KZ', label=_('Телефон'), required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(widget=DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
                                 required=False, label=_('Дата рождения'))

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'sex',
            'is_active',
            'email',
            'phone_number',
            'birth_date',
            'iin',
            'address',
            'password',
            'password_confirm',
        )
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя')}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Фамилия')}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': _('Почта')}),
            'iin': TextInput(attrs={'class': 'form-control', 'placeholder': 'ИИН'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': _('Адрес')}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if Account.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError({'email': _('Пользователь с такой почтой уже существует')})
        if Account.objects.filter(phone_number=cleaned_data.get('phone_number')).exists():
            raise ValidationError({'phone_number': _('Пользователь с таким телефоном уже существует')})
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError(_('Пароли не совпадают'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user
