
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from django.utils.translation import gettext_lazy as _

from api.serializers import ApplicationUpdateSerializer
from applications.models import Application
from applications.services.statuses import set_application_status


class IsSuperUserOrAdmin(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user.groups.filter(name='admin').exists() or request.user.is_superuser)


class SaveApplication(ModelViewSet):
    permission_classes = [IsSuperUserOrAdmin, ]
    serializer_class = ApplicationUpdateSerializer
    required_fields = ['applicant_name', 'applicant_surname', 'email', 'phone', 'school', 'class_number', 'shift',
                       'birth_date', 'sex', 'parents_surname', 'parents_name', 'parents_inn', 'parents_email',
                       'address', 'lesson_time', 'subjects', 'sum']

    def update(self, request, *args, **kwargs):
        data = {'form': _('Сохранено')}
        application = get_object_or_404(Application, pk=kwargs.get('pk'))
        serializer = self.get_serializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        if all(getattr(application, field) for field in self.required_fields):
            status_name = _('Подписание договора')
            data['result'] = 'success'
        else:
            status_name = _('В работе')
            data['result'] = 'bad'
        set_application_status(application=application, status_name=status_name, author=request.user)
        data['status'] = status_name
        return JsonResponse(data)


class SaveApplicantContract(ModelViewSet):
    permission_classes = [IsSuperUserOrAdmin, ]
    serializer_class = ApplicationUpdateSerializer

    def update(self, request, *args, **kwargs):
        data = {}
        application = get_object_or_404(Application, pk=kwargs.get('pk'))
        serializer = self.get_serializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        if not application.contract:
            status_name = _('Подписание договора')
            data['result'] = 'bad'
        else:
            status_name = _('Ожидание оплаты')
            data['result'] = 'success'
        set_application_status(application=application, status_name=status_name, author=request.user)
        data['contract_url'] = str(application.contract)
        data['form'] = _('Сохранено')
        data['status'] = status_name
        return JsonResponse(data, status=200)


class SaveApplicationPayedInfo(ModelViewSet):
    permission_classes = [IsSuperUserOrAdmin, ]
    serializer_class = ApplicationUpdateSerializer

    def update(self, request, *args, **kwargs):
        data = {}
        application = get_object_or_404(Application, pk=kwargs.get('pk'))
        serializer = self.get_serializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        if application.payed is True:
            status_name = _('Оплачена')
            data['result'] = 'success'
        else:
            status_name = _('Ожидание оплаты')
            data['result'] = 'bad'
        set_application_status(application=application, status_name=status_name, author=request.user)
        data['form'] = _('Сохранено')
        data['status'] = status_name
        return JsonResponse(data)
