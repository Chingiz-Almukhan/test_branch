from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from education.models import Discount


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('name', 'discount_amount')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Название льготы')}),
            'discount_amount': TextInput(
                attrs={'class': 'form-control', 'type': 'number', 'placeholder': _('Размер в %')}
                ),
        }
