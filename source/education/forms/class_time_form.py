from django import forms

from education.models import ClassTime


class ClassTimeForm(forms.ModelForm):
    class Meta:
        model = ClassTime
        fields = ('time_start', 'time_end')
