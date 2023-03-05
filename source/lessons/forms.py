from django import forms

from lessons.models import Homework


class HomeworkForm(forms.ModelForm):

    class Meta:
        model = Homework
        fields = ('task', 'attachment')
