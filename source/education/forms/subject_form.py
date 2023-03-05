from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _


from education.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'is_deleted')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Название предмета')}),
        }
