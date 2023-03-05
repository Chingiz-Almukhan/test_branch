from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, View

from accounts.models import Account, Teacher

from education.forms.grouping_form import GroupingForm
from education.models import (Grouping, Schedule, StudentGrouping, Subject,
                              TeacherGrouping)
from lessons.models import Lesson
from students.models import StudentContract


class GroupingListView(LoginRequiredMixin, ListView):
    template_name = 'education/groupings.html'
    model = Grouping
    context_object_name = 'groupings'

    def get_queryset(self, *args, **kwargs):
        return Grouping.objects.filter(is_deleted=False).order_by('-pk')


class GroupingAddView(LoginRequiredMixin, CreateView):
    template_name = 'education/grouping_add.html'
    model = Grouping
    form_class = GroupingForm

    def get_success_url(self):
        return reverse('groupings')


class GroupingEditView(LoginRequiredMixin, UpdateView):
    template_name = 'education/grouping_update.html'
    model = Grouping
    form_class = GroupingForm
    context_object_name = 'grouping'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grouping_subject: Subject = self.get_object().subject

        teachers = Teacher.objects.filter(subjects=grouping_subject)
        context['teachers'] = teachers

        similar_groups = Grouping.objects.filter(subject=grouping_subject, is_deleted=False)
        students_similar_groupings = StudentGrouping.objects.filter(grouping__in=similar_groups, is_active=True)

        students_contracts = StudentContract.objects.filter(subjects=grouping_subject, is_active=True)
        students_with_grouping_subject = Account.objects.filter(student_contracts__in=students_contracts)
        students = Account.objects.exclude(student_grouping__in=students_similar_groupings).filter(
                                           pk__in=students_with_grouping_subject)
        context['students'] = students

        students_in_grouping = self.get_object().student_grouping.filter(is_active=True)
        context['students_in_grouping'] = students_in_grouping

        message = self.request.session.get('message', '')
        context['message'] = message

        teacher_message = self.request.session.get('teacher_message', '')
        context['teacher_message'] = teacher_message

        if 'message' in self.request.session:
            del self.request.session['message']
        if 'teacher_message' in self.request.session:
            del self.request.session['teacher_message']

        if self.request.session.get('tab'):
            tab = self.request.session.get('tab')
            context['tab'] = tab
            del self.request.session['tab']
        else:
            context['tab'] = 0

        return context

    def get_success_url(self):
        return reverse('groupings')


@login_required
def remove_teacher_from_grouping_view(request, pk):
    grouping: Grouping = get_object_or_404(Grouping, pk=pk)
    teacher_grouping: TeacherGrouping = TeacherGrouping.objects.get(is_active=True, grouping=grouping)
    finished_at = request.POST.get('finished_at')
    teacher_grouping.finished_at = finished_at
    teacher_grouping.is_active = False
    teacher_grouping.save()
    lessons = Lesson.objects.filter(date__gte=finished_at, grouping=grouping)
    for lesson in lessons:
        lesson.teacher = None
        lesson.save()
    request.session['tab'] = 1
    teacher_pk = teacher_grouping.teacher.pk
    if 'grouping' in request.META.get('HTTP_REFERER'):
        return redirect('grouping_update', pk)
    else:
        return redirect('teacher', teacher_pk)


@login_required
def add_teacher_to_grouping_view(request):
    grouping_pk = request.POST.get('grouping_pk')
    grouping: Grouping = get_object_or_404(Grouping, pk=grouping_pk)
    teacher_pk: str = request.POST.get('teacher_pk')
    teacher: Teacher = get_object_or_404(Teacher, pk=teacher_pk)
    started_at: str = request.POST.get('started_at')
    schedules = Schedule.objects.filter(grouping=grouping, is_deleted=False)
    week_days_dict = {
        'monday': 'понедельник',
        'tuesday': 'вторник',
        'wednesday': 'среду',
        'thursday': 'четверг',
        'friday': 'пятницу',
        'saturday': 'субботу',
        'sunday': 'воскресенье',
    }
    request.session['tab'] = 1
    teacher_groupings = TeacherGrouping.objects.filter(teacher=teacher, is_active=True)
    overlapping_schedules = [
        Schedule.objects.filter(grouping=teacher_grouping.grouping, week_day=schedule.week_day,
                                class_time=schedule.class_time, is_deleted=False)
        for teacher_grouping in teacher_groupings
        for schedule in schedules
    ]
    if any(overlapping_schedules):
        message = ''
        for schedule in overlapping_schedules:
            for group in schedule:
                message += f"{group.grouping.name} в {week_days_dict[group.week_day]} в \
                {group.class_time.time_start}, в группе "
        request.session['teacher_message'] = f'Преподаватель {teacher} уже ведет занятие в группе {message[:-11]}'

        if 'grouping' in request.META.get('HTTP_REFERER'):
            return redirect('grouping_update', grouping.pk)
        else:
            return redirect('teacher', teacher_pk)

    TeacherGrouping.objects.create(grouping=grouping, teacher=teacher, started_at=started_at)
    lessons = Lesson.objects.filter(date__gte=started_at, grouping=grouping)
    for lesson in lessons:
        lesson.teacher = teacher
        lesson.save()

    if 'grouping' in request.META.get('HTTP_REFERER'):
        return redirect('grouping_update', grouping.pk)
    else:
        return redirect('teacher', teacher_pk)


class DelGroupingView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        grouping = get_object_or_404(Grouping, pk=kwargs['pk'])
        grouping.is_deleted = True
        grouping.save()
        return redirect('groupings')
