from django import forms

from students.models import Payment


class DateInput(forms.DateInput):
    input_type = 'date'


class PaymentCreateForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(format='%Y-%m-%d', attrs={'class': 'form-control'}),
                           label='Дата платежа')

    class Meta:
        model = Payment
        fields = (
            'date',
            'amount',
        )
