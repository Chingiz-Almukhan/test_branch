from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from education.models import Packet


class PackageForm(forms.ModelForm):
    class Meta:
        model = Packet
        fields = ('name', 'qty', 'sum')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Название пакета')}),
            'qty': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': _('Количество предметов')}),
            'sum': TextInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'Сумма'}),
        }
