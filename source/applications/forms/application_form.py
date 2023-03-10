from django import forms
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from applications.models import Application

from education.models import Subject


class ApplicationSendForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(label=_('Желаемые предметы'),
                                              queryset=Subject.objects.filter(is_deleted=False),
                                              widget=forms.CheckboxSelectMultiple(
                                                  attrs={
                                                      'class': 'subject-check',
                                                  }))
    email = forms.CharField(required=True, label='Email', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Email',
        }))
    applicant_name = forms.CharField(required=True, label=_('Имя'), widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Имя'),
        }))
    applicant_surname = forms.CharField(required=True, label=_('Фамилия'), widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': _('Фамилия'),
        }))
    phone = PhoneNumberField(region='KZ', label='Телефон', required=True)

    class Meta:
        model = Application
        fields = ('applicant_name', 'applicant_surname', 'email', 'phone', 'subjects')

    def save(self, commit=True):
        application = super().save(commit=True)
        application.save()
        return application
