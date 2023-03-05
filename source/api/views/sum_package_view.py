from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from api.views.application_first_form import IsSuperUserOrAdmin
from education.models import Packet, Discount


class SumPackageView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        if request.POST.get('package'):
            get_package = get_object_or_404(Packet, qty=request.POST.get('package'))
            data['sum'] = get_package.sum
            data['package'] = get_package.name.lower()
        return JsonResponse(data)


class SumDiscountView(APIView):
    permission_classes = [IsSuperUserOrAdmin, ]

    def post(self, request, *args, **kwargs):
        data = {}
        if request.POST.get('subject'):
            get_package = get_object_or_404(Packet, qty=request.POST.get('subject'))
            try:
                get_discount = get_object_or_404(Discount, pk=request.POST.get('discount'))
                total = int(get_package.sum) - ((int(get_package.sum) * int(get_discount.discount_amount)) / 100)
                data['total'] = total
                data['discount'] = get_discount.discount_amount
            except ValueError:
                data['return_sum'] = get_package.sum
        return JsonResponse(data)
