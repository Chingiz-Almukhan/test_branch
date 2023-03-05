from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from accounts.models import Account
from api.views.application_first_form import IsSuperUserOrAdmin
from applications.models import Application
from applications.services.statuses import set_application_status
from students.models import Payment
from students.models import StudentContract


class CreateStudent(APIView):
    permission_classes = [IsSuperUserOrAdmin, ]

    def post(self, request, *args, **kwargs):
        data = {}
        default_password = '1234'
        application = get_object_or_404(Application, pk=kwargs.get('pk'))
        if Account.objects.filter(email=application.email).exists():
            data['email'] = _('Пользователь с такой почтой уже существует')
            return JsonResponse(data)
        if Account.objects.filter(phone_number=application.phone).exists():
            data['phone'] = _('Пользователь с таким номером телефона уже существует')
            return JsonResponse(data)
        student = Account.objects.create(first_name=application.applicant_name, last_name=application.applicant_surname,
                                         email=application.email, phone_number=application.phone,
                                         application=application, birth_date=application.birth_date,
                                         address=application.address, sex=application.sex)
        student.set_password(default_password)
        student.save()
        group = Group.objects.get(name='student')
        student.groups.add(group)
        student_contract = StudentContract.objects.create(student=student, signing_date=application.contract_date,
                                                          start_date=application.contract_date,
                                                          contract=application.contract,
                                                          amount=application.sum, is_active=True)
        student_contract.subjects.set(application.subjects.all())
        Payment.objects.create(student=student, amount=application.sum, author=request.user)
        set_application_status(application=application, status_name=_('Завершена'), author=request.user)
        send_mail(
            'Quantum registration',
            f'Quatum saitynda sizdin tirkelgininizdi habarlaimyz \
                \
            login - {application.email} password - {default_password}\
            \
            Qupiya sozdi aystyrudy suraimyz',
            'testeruly@yandex.kz',
            [application.email],
            fail_silently=False,
        )

        data['success'] = _('Студент создан')
        return JsonResponse(data)
