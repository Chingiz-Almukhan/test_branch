from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, View

from education.forms.discount_form import DiscountForm
from education.models import Discount


class DiscountListView(LoginRequiredMixin, ListView):
    template_name = 'education/discounts.html'
    model = Discount
    context_object_name = 'discounts'

    def get_queryset(self, *args, **kwargs):
        return Discount.objects.filter(is_deleted=False).order_by('pk')


class DiscountAddView(LoginRequiredMixin, CreateView):
    template_name = 'education/discount_add.html'
    form_class = DiscountForm
    model = Discount

    def get_success_url(self):
        return reverse('discounts')


class DiscountEditView(LoginRequiredMixin, UpdateView):
    template_name = 'education/discount_update.html'
    model = Discount
    form_class = DiscountForm
    context_object_name = 'discount'

    def get_success_url(self):
        return reverse('discounts')


class DelDiscountView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        package = get_object_or_404(Discount, pk=kwargs['pk'])
        package.is_deleted = True
        package.save()
        return redirect('discounts')
