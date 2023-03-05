from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView

from accounts.models import Account
from accounts.models.account import Teacher
from education.forms.schedule_create import ScheduleForm
from education.models import (Auditorium, ClassTime, Grouping, Schedule,
                              StudentGrouping)
from education.models.grouping import TeacherGrouping


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'education/schedule_create.html'
    model = Schedule
    form_class = ScheduleForm

    def get_success_url(self):
        return reverse('crm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(name='student')
        students = Account.objects.filter(groups=group)
        auditoriums = Auditorium.objects.all()
        teachers = Teacher.objects.all()
        sum_dict = {'108': {}, '109': {}, '110': {}}
        for auditorium in auditoriums:
            schedules = auditorium.schedules.filter(is_deleted=False)
            my_dict = {'monday': {}, 'tuesday': {}, 'wednesday': {}, 'thursday': {}, 'friday': {}, 'saturday': {}}
            for schedule in schedules:
                my_dict[schedule.week_day][schedule.class_time.number_lesson] = schedule.grouping.name
            sum_dict[auditorium.name] = my_dict
        context['sum_dict'] = sum_dict
        groupings = Grouping.objects.filter(is_deleted=False)
        context['groupings'] = groupings
        context['students'] = students
        context['teachers'] = teachers

        message = self.request.session.get('message', '')
        context['message'] = message
        if 'message' in self.request.session:
            del self.request.session['message']

        return context

    def post(self, request, *args, **kwargs):
        form = ScheduleForm(request.POST)
        auditorium_pk = request.POST.get('auditorium')
        auditorium = get_object_or_404(Auditorium, pk=auditorium_pk)
        week_day = request.POST.get('week_day')
        class_time_pk = request.POST.get('class_time')
        class_time = get_object_or_404(ClassTime, pk=class_time_pk)
        if Schedule.objects.filter(auditorium=auditorium, class_time=class_time,
                                   week_day=week_day, is_deleted=False).exists():
            schedule = get_object_or_404(Schedule, auditorium=auditorium, class_time=class_time,
                                         week_day=week_day, is_deleted=False)
            schedule.is_deleted = True
            schedule.save()
        if form.is_valid():
            grouping_pk: str = request.POST.get('grouping')
            if grouping_pk:
                grouping = get_object_or_404(Grouping, pk=grouping_pk)
                if Schedule.objects.filter(grouping=grouping, class_time=class_time,
                                           week_day=week_day, is_deleted=False).exists():
                    request.session['message'] = f'У группы {grouping} уже есть расписание в это время'

                else:
                    form.save()
        return redirect('schedule_create')


@login_required
def schedule_generate_view(request):
    """"""
    # очищает текущее расписание
    schedules = Schedule.objects.filter(is_deleted=False)
    for schedule in schedules:
        schedule.is_deleted = True
        schedule.save()

    groupings = Grouping.objects.filter(is_deleted=False)
    # Цикл добавления расписание группам
    for grouping in groupings:
        week_day, auditorium, class_time = get_first_availible_cell(week_days=('monday', 'tuesday', 'wednesday'))
        Schedule.objects.create(grouping=grouping, week_day=week_day, class_time=class_time, auditorium=auditorium)

        week_day, auditorium, class_time = get_first_availible_cell(week_days=('thursday', 'friday', 'saturday'))
        Schedule.objects.create(grouping=grouping, week_day=week_day, class_time=class_time, auditorium=auditorium)

    return redirect('schedule_create')


def get_first_availible_cell(week_days: tuple[str]) -> tuple[str, Auditorium, ClassTime]:
    """Находит первую пустую ячейку в сочетании трех значений аудитория, день недели и номер урока"""
    class_times = ClassTime.objects.all()
    auditoriums = Auditorium.objects.all()
    for week_day in week_days:
        for auditorium in auditoriums:
            for class_time in class_times:
                if not Schedule.objects.filter(auditorium=auditorium, class_time=class_time,
                                               week_day=week_day, is_deleted=False).exists():
                    return (week_day, auditorium, class_time)


@login_required
def set_schedule_not_active(request):
    Schedule.objects.update(is_deleted=True)
    return redirect('schedule_create')


@login_required
def get_student_groupings_view(request, student_pk):
    student = get_object_or_404(Account, pk=student_pk)
    student_in_groupings = StudentGrouping.objects.filter(student=student, is_active=True)
    groupings = []
    for student_in_grouping in student_in_groupings:
        groupings.append(student_in_grouping.grouping.name)
    data = {'groupings': groupings}
    return JsonResponse(data)


@login_required
def get_teacher_groupings_view(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    teacher_in_groupings = TeacherGrouping.objects.filter(teacher=teacher, is_active=True)
    groupings = []
    for teacher_in_grouping in teacher_in_groupings:
        groupings.append(teacher_in_grouping.grouping.name)
    data = {'groupings': groupings}
    return JsonResponse(data)
