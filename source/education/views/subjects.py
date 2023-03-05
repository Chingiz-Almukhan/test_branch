from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, View

from education.forms.subject_form import SubjectForm
from education.models import Subject


class SubjectListView(LoginRequiredMixin, ListView):
    template_name = 'education/subjects.html'
    model = Subject
    context_object_name = 'subjects'

    def get_queryset(self, *args, **kwargs):
        return Subject.objects.filter(is_deleted=False).order_by('name')


class SubjectAddView(LoginRequiredMixin, CreateView):
    template_name = 'education/subject_add.html'
    form_class = SubjectForm
    model = Subject

    def get_success_url(self):
        return reverse('subjects')


class SubjectEditView(LoginRequiredMixin, UpdateView):
    template_name = 'education/subject_update.html'
    model = Subject
    form_class = SubjectForm
    context_object_name = 'subject'

    def get_success_url(self):
        return reverse('subjects')


class DelSubjectView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=kwargs['pk'])
        subject.is_deleted = True
        subject.save()
        return redirect('subjects')
