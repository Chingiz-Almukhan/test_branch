from django import forms

from students.models import MedicalCertificate


class DateInput(forms.DateInput):
    input_type = 'date'


class MedicalCertificateForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(format='%Y-%m-%d', attrs={'class': 'form-control'}),
                                 label='Дата начала')
    end_date = forms.DateField(widget=DateInput(format='%Y-%m-%d', attrs={'class': 'form-control'}),
                               label='Дата окончания')

    class Meta:
        model = MedicalCertificate
        fields = (
            'start_date',
            'end_date',
            'attachment',
        )
