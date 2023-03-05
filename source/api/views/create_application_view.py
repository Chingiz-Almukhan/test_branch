from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from django.utils.translation import gettext_lazy as _

from api.serializers import ApplicationCreateSerializer
from applications.models import Application, Status


class AddApplicationView(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer

    def create(self, request, *args, **kwargs):
        data = {}
        if request.data['phone']:
            request.data._mutable = True
            if request.data['phone'][0] == "+":
                phone = request.data['phone']
            else:
                phone = '+7' + request.data['phone'][1:]
            request.data['phone'] = phone
            request.data._mutable = False
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if Application.objects.filter(applicant_name=request.data['applicant_name'],
                                          applicant_surname=request.data['applicant_surname'],
                                          phone=request.data['phone'],
                                          email=request.data['email'], subjects=request.POST.get('subjects')).exists():
                data['invalid'] = _('Вы уже оставили заявку')
                data['invalid_id'] = 'exists'
            else:
                get_status = Status.objects.get(name=_('Создана'))
                serializer.save()
                serializer.instance.statuses.add(get_status)
                data['success'] = _('Заявка создана')
        else:
            if serializer.errors.get('phone'):
                data['phone'] = serializer.errors.get('phone')
            elif serializer.errors.get("applicant_name"):
                data['applicant_name'] = _('Укажите имя')
            elif serializer.errors.get("applicant_surname"):
                data['applicant_surname'] = _('Укажите фамилию')
            elif serializer.errors.get("email"):
                data['email'] = _('Укажите почту')
            else:
                data['subject'] = _('Выберете предмет')
                data['subject_id'] = 'subject_error'
        return JsonResponse(data)
