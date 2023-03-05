from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput, TextInput
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from applications.models import StudentSex


class StudentEditForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=StudentSex.choices,
                            widget=forms.Select(attrs={'class': 'form-control', 'placeholder': _('Пол')}))
    phone_number = PhoneNumberField(region='KZ', label='Телефон', required=True,
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
        )
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя')}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Фамилия')}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': _('Почта')}),
            'iin': TextInput(attrs={'class': 'form-control', 'placeholder': 'ИИН'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': _('Адрес')}),
        }
