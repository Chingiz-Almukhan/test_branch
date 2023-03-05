from django import forms

from education.models import Grouping, Schedule


class ScheduleForm(forms.ModelForm):
    grouping = forms.ModelChoiceField(
        queryset=Grouping.objects.filter(is_deleted=False),
        required=False,
    )

    class Meta:
        model = Schedule
        fields = ('grouping', 'week_day', 'class_time', 'auditorium')
        widgets = {
            'week_day': forms.Select(attrs={'hidden': True}),
            'class_time': forms.Select(attrs={'hidden': 'True'}),
            'auditorium': forms.Select(attrs={'hidden': 'True'}),
        }
