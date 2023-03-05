from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView

from accounts.models import Account
from accounts.models.account import Teacher

from education.models import Grouping, StudentGrouping

from lessons.forms import HomeworkForm
from lessons.models import Lesson


class CalendarView(LoginRequiredMixin, TemplateView):
    """Отображение календаря"""
    template_name = "lessons/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user: Account = self.request.user

        # определяем какой пользователь делает запрос, чтобы сформировать для него его занятия
        if user.groups.filter(name='student').exists():
            students_groupings = user.student_grouping.filter(is_active=True)

            # формирование списка из querysetов для их дальнейших объединений в один queryset занятий
            # список формируется на основе всех занятий всех групп студента
            querysets = []
            for student_grouping in students_groupings:
                querysets.append(student_grouping.grouping.lessons.all())

            # объединение списка querysetов в один общий queryset
            if querysets:
                combined_condition = Q()
                for qs in querysets:
                    combined_condition |= Q(pk__in=qs)
                lessons = Lesson.objects.filter(combined_condition)
            else:  # если нет групп у студента в lessons записываем пустой кверисет
                lessons = Lesson.objects.none()

        elif user.groups.filter(name='teacher').exists():
            lessons = user.teacher.lessons.all()

        else:
            lessons = Lesson.objects.all()

        lesson_list = []
        pay_notification = []
        for lesson in lessons:
            lesson_date = lesson.date
            lesson_time = lesson.class_time.time_start
            lesson_datetime = datetime.combine(lesson_date, lesson_time)
            lesson_list.append(
                {
                    'title': lesson.auditorium.name + ' ' + lesson.grouping.name,
                    'start': lesson_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                    'id': lesson.pk,
                    'color': 'coral',
                    'url': f'/lesson/{lesson.pk}',
                },
                )
            pay_notification.append(f'{lesson_datetime.strftime("%Y-%m")}-10')
        context['events'] = lesson_list
        if user.groups.filter(name='student').exists():
            for i in set(pay_notification):
                lesson_list.append(
                    {
                        'title': 'Уведомление об оплате',
                        'start': i,
                        'color': 'red',
                    },
                )
        return context


class LessonDetailView(LoginRequiredMixin, DetailView):
    template_name = 'lessons/lesson-detail.html'
    model = Lesson
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        studentsgroupings = StudentGrouping.objects.filter(grouping=self.get_object().grouping, is_active=True)
        context['studentsgroupings'] = studentsgroupings
        homework_form = HomeworkForm(instance=self.get_object().homework)
        context['homework_form'] = homework_form
        lesson = get_object_or_404(Lesson, pk=self.object.pk)
        students_in_lesson = lesson.students_visited.all()
        if self.request.user in students_in_lesson:
            context['student_in_lesson'] = True
        teachers = Teacher.objects.filter(subjects=lesson.grouping.subject)
        context['teachers'] = teachers
        return context


def update_teacher_in_lesson_view(request):
    teacher_pk = request.POST.get('teacher_pk')
    lesson_pk = request.POST.get('lesson_pk')
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    lesson.teacher = teacher
    lesson.save()
    return redirect('lesson-detail', lesson_pk)


@login_required
def lesson_edit_view(request, lesson_pk):
    students_in_lesson = dict(request.POST).get('students')
    lesson = get_object_or_404(Lesson, pk=lesson_pk)

    if students_in_lesson is None:
        lesson.students_visited.clear()
    else:
        lesson.students_visited.set(students_in_lesson)
    lesson_topic: str = dict(request.POST).get('topic')[0]
    lesson.topic = lesson_topic

    homework_form = HomeworkForm(request.POST, request.FILES, instance=lesson.homework)

    lesson_is_conducted = dict(request.POST).get('is_conducted')
    if lesson_is_conducted:
        lesson.is_conducted = True
    else:
        lesson.is_conducted = False

    if homework_form.is_valid():
        homework = homework_form.save()
        lesson.homework = homework

    lesson.save()

    return redirect('lesson-detail', pk=lesson_pk)


@login_required
def lessons_generate_view(request):
    start_date_from_request: str = dict(request.POST).get('start_date')[0]
    end_date_from_request: str = dict(request.POST).get('end_date')[0]
    week_days = {
        'monday': [],
        'tuesday': [],
        'wednesday': [],
        'thursday': [],
        'friday': [],
        'saturday': [],
        'sunday': [],
    }
    index_week_days = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday',
    }

    start_date = datetime.strptime(start_date_from_request, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_from_request, '%Y-%m-%d')
    period = end_date - start_date + timedelta(days=1)
    for i in range(period.days):
        dt = start_date + timedelta(i)
        index_week_day: int = datetime.weekday(dt)
        name_week_day: str = index_week_days.get(index_week_day)
        week_days.get(name_week_day).append(dt)

    groupings = Grouping.objects.filter(is_deleted=False)
    for grouping in groupings:
        for schedule in grouping.schedules.filter(is_deleted=False):
            week_day: str = schedule.week_day
            lesson_dates: list = week_days.get(week_day)

            try:
                teacher = grouping.teacher_groupings.filter(is_active=True)[0].teacher
            except IndexError:
                teacher = None

            for lesson_date in lesson_dates:
                if not Lesson.objects.filter(
                        date=lesson_date,
                        auditorium=schedule.auditorium,
                        class_time=schedule.class_time,
                ).exists():
                    lesson = Lesson(date=lesson_date, auditorium=schedule.auditorium,
                                    class_time=schedule.class_time, teacher=teacher, grouping=grouping)
                else:
                    lesson: Lesson = Lesson.objects.get(date=lesson_date, auditorium=schedule.auditorium,
                                                        class_time=schedule.class_time)
                    lesson.grouping = grouping
                    lesson.teacher = teacher

                lesson.save()

    return redirect('crm')
