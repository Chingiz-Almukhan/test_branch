from django import forms
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from education.models import Grouping, Subject


class GroupingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(is_deleted=False)

    class Meta:
        model = Grouping
        fields = ('name', 'subject')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Название группы')}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }
