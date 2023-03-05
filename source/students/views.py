from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import Account

from education.models import Grouping, Schedule, StudentGrouping, Subject

from lessons.models import Lesson

from students.forms.medical_certificate import MedicalCertificateForm
from students.forms.payment import PaymentCreateForm
from students.forms.student_edit_form import StudentEditForm
from students.forms.student_form import StudentForm
from students.models import FundsDebiting, MedicalCertificate, Payment, StudentContract



@login_required
def student_detail_view(request):
    student = get_object_or_404(Account, pk=request.user.pk)
    context = {}
    context['student'] = student
    return render(request=request, template_name='students/student_detail.html', context=context)


@login_required
def student_payments_view(request):
    context = {}

    student = get_object_or_404(Account, pk=request.user.pk)
    context['student'] = student

    student_payments = Payment.objects.filter(student=student)
    total_payments = student_payments.aggregate(Sum('amount'))['amount__sum']
    context['total_payments'] = total_payments

    student_fundsdebitings = FundsDebiting.objects.filter(student=student)
    total_fundsdebitings = student_fundsdebitings.aggregate(Sum('amount'))['amount__sum']
    context['total_fundsdebitings'] = total_fundsdebitings

    return render(request=request, template_name='students/student_payments.html', context=context)


@login_required
def student_groupings_view(request):
    student = get_object_or_404(Account, pk=request.user.pk)
    groupings = Grouping.objects.filter(student_grouping__student=student, student_grouping__is_active=True)
    students = StudentGrouping.objects.filter(grouping__in=groupings, is_active=True)
    context = {}
    context['student'] = student
    context['students'] = students
    context['student_groupings'] = groupings
    return render(request=request, template_name='students/student_groupings.html', context=context)


@login_required
def student_homeworks_view(request):
    student = get_object_or_404(Account, pk=request.user.pk)
    groupings = Grouping.objects.filter(student_grouping__student=student, student_grouping__is_active=True)
    lessons = Lesson.objects.filter(grouping__in=groupings)
    context = {}
    context['student'] = student
    context['lessons'] = lessons
    return render(request=request, template_name='students/student_homeworks.html', context=context)


class StudentListView(LoginRequiredMixin, ListView):
    template_name = 'students/admin/students.html'
    model = Account
    context_object_name = 'students'

    def get_queryset(self, *args, **kwargs):
        return Account.objects.filter(groups__name='student').order_by('-pk')


# TODO данный вью не используется, принять решение по нему
class StudentAddView(LoginRequiredMixin, CreateView):
    template_name = 'students/admin/student_create.html'
    form_class = StudentForm
    model = Account

    def post(self, request, *args, **kwargs):
        group = Group.objects.get(name='student')
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(group)
            return redirect('students')
        context = {'form': form}
        return self.render_to_response(context)


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'students/admin/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student: Account = self.get_object()

        payments = Payment.objects.filter(student=student)
        context['payments'] = payments

        student_groupings = StudentGrouping.objects.filter(student=student, is_active=True)
        groupings_by_student = Grouping.objects.filter(student_grouping__in=student_groupings, is_deleted=False)
        lessons = Lesson.objects.filter(grouping__in=groupings_by_student)
        context['lessons'] = lessons

        if StudentContract.objects.filter(is_active=True, student=student).exists():
            student_subjects = StudentContract.objects.get(is_active=True, student=student).subjects.all()
            student_groupings_subjects = Subject.objects.filter(groupings__in=student.get_active_groupings())
            groupings = Grouping.objects.filter(
                is_deleted=False,
                subject__in=student_subjects).exclude(subject__in=student_groupings_subjects)
        else:
            groupings = Grouping.objects.none()
        context['groupings'] = groupings

        student_payments = Payment.objects.filter(student=student)
        total_payments = student_payments.aggregate(Sum('amount'))['amount__sum']
        if total_payments is None:
            total_payments = 0
        context['total_payments'] = total_payments

        student_fundsdebitings = FundsDebiting.objects.filter(student=student)
        total_fundsdebitings = student_fundsdebitings.aggregate(Sum('amount'))['amount__sum']
        if total_fundsdebitings is None:
            total_fundsdebitings = 0
        context['total_fundsdebitings'] = total_fundsdebitings

        balance = total_payments - total_fundsdebitings
        context['balance'] = balance

        if student.get_active_contract():
            contract_amount = student.get_active_contract().amount
            if balance >= contract_amount:
                next_payment = 0
            else:
                next_payment = contract_amount - balance
            context['next_payment'] = next_payment

        medical_certificate_form = MedicalCertificateForm()
        context['medical_certificate_form'] = medical_certificate_form

        payment_form = PaymentCreateForm()
        context['payment_form'] = payment_form

        message = self.request.session.get('message', '')
        context['message'] = message
        if 'message' in self.request.session:
            del self.request.session['message']
        tab = self.request.session.get('tab')
        context['tab'] = tab
        if 'tab' in self.request.session:
            del self.request.session['tab']
        else:
            context['tab'] = 0

        return context


class StudentEditView(LoginRequiredMixin, UpdateView):
    template_name = 'students/admin/student_update.html'
    model = Account
    form_class = StudentEditForm
    context_object_name = 'student'

    def get_success_url(self):
        return reverse('students')


class MedicalCertificateCreateView(LoginRequiredMixin, CreateView):
    form_class = MedicalCertificateForm
    model = MedicalCertificate

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Account, pk=kwargs.get('pk'))
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            medical_certificate: MedicalCertificate = form.save(commit=False)
            medical_certificate.student = student
            medical_certificate.author = request.user
            medical_certificate.save()
        return redirect('student', self.kwargs['pk'])


class PaymentCreateView(LoginRequiredMixin, CreateView):
    form_class = PaymentCreateForm
    model = Payment

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Account, pk=kwargs.get('pk'))
        form = self.form_class(request.POST)
        if form.is_valid():
            payment: Payment = form.save(commit=False)
            payment.student = student
            payment.author = request.user
            payment.save()
        return redirect('student', self.kwargs['pk'])


@login_required
def add_student_to_grouping_view(request, **kwargs):
    grouping_pk = request.POST.get('grouping_pk')
    grouping: Grouping = get_object_or_404(Grouping, pk=grouping_pk)
    student_pk: str = request.POST.get('student_pk')
    enrolled_at = request.POST.get('enrolled_at')

    student: Account = get_object_or_404(Account, pk=student_pk)
    request.session['tab'] = 2

    week_days_dict = {
        'monday': 'понедельник',
        'tuesday': 'вторник',
        'wednesday': 'среду',
        'thursday': 'четверг',
        'friday': 'пятницу',
        'saturday': 'субботу',
        'sunday': 'воскресенье',
    }

    schedules = Schedule.objects.filter(grouping=grouping, is_deleted=False)
    student_groupings = StudentGrouping.objects.filter(student=student, is_active=True)
    groupings_by_student_count = StudentGrouping.objects.filter(student=student, is_active=True).count()
    students_by_grouping_count = StudentGrouping.objects.filter(grouping=grouping, is_active=True).count()

    redirect_flag = False
   
    if groupings_by_student_count >= 4:
        request.session['message'] = f'Ученик {student} уже зачислен в {groupings_by_student_count} группах'
        redirect_flag = True

    if students_by_grouping_count >= 12:
        request.session['message'] = f'В группе {grouping} уже зачислено {students_by_grouping_count} учеников'
        redirect_flag = True

    if redirect_flag:
        if 'grouping' in request.META.get('HTTP_REFERER'):
            return redirect('grouping_update', grouping.pk)
        else:
            return redirect('student', student.pk)

    overlapping_schedules = [
        Schedule.objects.filter(grouping=student_grouping.grouping, week_day=schedule.week_day,
                                class_time=schedule.class_time, is_deleted=False)
        for student_grouping in student_groupings
        for schedule in schedules
    ]
    if any(overlapping_schedules):
        message = ''
        for schedule in overlapping_schedules:
            for group in schedule:
                message += f"{group.grouping.name} в {week_days_dict[group.week_day]} в \
                 {group.class_time.time_start}, в группе "
        request.session['message'] = f'У студента {student} уже есть занятие в группе {message[:-11]}'
        if 'grouping' in request.META.get('HTTP_REFERER'):
            return redirect('grouping_update', grouping.pk)
        else:
            return redirect('student', student.pk)

    if not StudentGrouping.objects.filter(grouping=grouping, student=student, is_active=True).exists():
        StudentGrouping.objects.create(grouping=grouping, student=student, enrolled_at=enrolled_at)

    if 'grouping' in request.META.get('HTTP_REFERER'):
        return redirect('grouping_update', grouping.pk)
    else:
        return redirect('student', student.pk)


@login_required
def del_student_from_grouping_view(request):
    grouping_pk = request.POST.get('grouping_pk')
    student_pk: str = request.POST.get('student_pk')
    expelled_at = request.POST.get('expelled_at')
    grouping: Grouping = get_object_or_404(Grouping, pk=grouping_pk)
    student: Account = get_object_or_404(Account, pk=student_pk)
    student_in_grouping = get_object_or_404(StudentGrouping, student=student, grouping=grouping, is_active=True)
    request.session['tab'] = 2
    student_in_grouping.is_active = False
    student_in_grouping.expelled_at = expelled_at
    student_in_grouping.save()
    if 'grouping' in request.META.get('HTTP_REFERER'):
        return redirect('grouping_update', grouping.pk)
    else:
        return redirect('student', student.pk)
