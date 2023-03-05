from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from accounts.models import Account
from api.views.application_first_form import IsSuperUserOrAdmin


class CheckUser(APIView):
    permission_classes = [IsSuperUserOrAdmin, ]

    def post(self, request, *args, **kwargs):
        data = {}
        if Account.objects.filter(email=request.POST.get('email')).exists() and Account.objects.filter(
                phone_number=request.POST.get('phone')).exists():
            data['email'] = _('Пользователь с такой почтой уже существует')
            data['phone'] = _('Пользователь с таким номером телефона уже существует')
            data['result'] = '1'
        elif Account.objects.filter(email=request.POST.get('email')).exists():
            data['email'] = _('Пользователь с такой почтой уже существует')
            data['result'] = '2'
        elif Account.objects.filter(phone_number=request.POST.get('phone')).exists():
            data['phone'] = _('Пользователь с таким номером телефона уже существует')
            data['result'] = '3'
        return JsonResponse(data)
