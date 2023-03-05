from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from accounts.models import Account, Teacher

from education.forms.teacher_edit_form import TeacherEditForm
from education.models import Grouping, Subject, TeacherGrouping


class TeachersListView(LoginRequiredMixin, ListView):
    template_name = 'education/teachers.html'
    model = Teacher
    context_object_name = 'teachers'

    def get_queryset(self, *args, **kwargs):
        return Teacher.objects.all().order_by('-pk')


class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'education/teacher.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher: Teacher = self.get_object()
        teacher_groupings = TeacherGrouping.objects.filter(is_active=True)
        groupings = Grouping.objects.filter(
            is_deleted=False,
            subject__in=teacher.subjects.all()).exclude(teacher_groupings__in=teacher_groupings)
        context['groupings'] = groupings
        teacher_message = self.request.session.get('teacher_message', '')
        context['teacher_message'] = teacher_message
        if 'teacher_message' in self.request.session:
            del self.request.session['teacher_message']

        if self.request.session.get('tab'):
            tab = self.request.session.get('tab')
            context['tab'] = tab
            del self.request.session['tab']
        else:
            context['tab'] = 0
        print(context)
        return context


class TeacherEditView(LoginRequiredMixin, UpdateView):
    template_name = 'education/teacher_update.html'
    model = Account
    form_class = TeacherEditForm
    context_object_name = 'teacher'

    def get_success_url(self):
        return reverse('teachers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.all()
        context['subjects'] = subjects
        return context

    def post(self, request, *args, **kwargs):
        subjects_pk = dict(request.POST).get('subject')
        self.get_object().teacher.subjects.set(subjects_pk)

        return super().post(request, *args, **kwargs)
