from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, View

from education.forms.package_form import PackageForm
from education.models import Packet


class PackageListView(LoginRequiredMixin, ListView):
    template_name = 'education/packages.html'
    model = Packet
    context_object_name = 'packages'

    def get_queryset(self, *args, **kwargs):
        return Packet.objects.filter(is_deleted=False).order_by('pk')


class PackageAddView(LoginRequiredMixin, CreateView):
    template_name = 'education/package_add.html'
    form_class = PackageForm
    model = Packet

    def get_success_url(self):
        return reverse('packages')


class PackageEditView(LoginRequiredMixin, UpdateView):
    template_name = 'education/package_update.html'
    model = Packet
    form_class = PackageForm
    context_object_name = 'package'

    def get_success_url(self):
        return reverse('packages')


class DelPackageView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        package = get_object_or_404(Packet, pk=kwargs['pk'])
        package.is_deleted = True
        package.save()
        return redirect('packages')
