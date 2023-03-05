from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, View)
from applications.forms.application_edit_form import (
    ApplicationContractEditForm, ApplicationCustomEditForm,
    ApplicationPayedEditForm, ApplicationRejectForm)
from applications.forms.application_form import ApplicationSendForm
from applications.models import Application, ApplicationStatus, Status
from applications.services.statuses import (get_button_status)
from accounts.permissions import AdminPassedTestMixin


class ApplicationEditView(LoginRequiredMixin, AdminPassedTestMixin, TemplateView):
    """Формирование контекста для отображения шаблона редактирования заявки"""

    template_name = 'applications/application_update.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationEditView, self).get_context_data(**kwargs)
        application = get_object_or_404(Application, pk=kwargs['pk'])
        context['application'] = application
        application_custom_form = ApplicationCustomEditForm(instance=application)
        application_contract_form = ApplicationContractEditForm(instance=application)
        application_payed_form = ApplicationPayedEditForm(instance=application)
        application_reject_form = ApplicationRejectForm(instance=application)
        context['application_custom_form'] = application_custom_form
        context['application_contract_form'] = application_contract_form
        context['application_payed_form'] = application_payed_form
        context['application_reject_form'] = application_reject_form
        button_status: dict[str, str] = get_button_status(application=application)

        context.update(button_status)
        return context


class ApplicationRejectView(LoginRequiredMixin, AdminPassedTestMixin, View):
    """Установка статуса Отклонена"""

    def post(self, *args, **kwargs):
        application = get_object_or_404(Application, pk=kwargs['pk'])
        status = get_object_or_404(Status, name='Отклонена')
        author = self.request.user
        form = ApplicationRejectForm(self.request.POST)
        application_status: ApplicationStatus = form.save(commit=False)
        application_status.application = application
        application_status.status = status
        application_status.author = author
        application_status.save()

        return redirect('application_update', self.kwargs['pk'])


class DeleteApplicationView(LoginRequiredMixin, AdminPassedTestMixin, View):
    def post(self, *args, **kwargs):
        subject = get_object_or_404(Application, pk=kwargs['pk'])
        subject.is_deleted = True
        subject.save()
        return redirect('applications_list')


class ApplicationDetailView(LoginRequiredMixin, AdminPassedTestMixin, DetailView):
    model = Application
    template_name = 'applications/application_detail.html'


class ApplicationsListView(LoginRequiredMixin, AdminPassedTestMixin, ListView):
    template_name = 'applications/applications_list.html'
    model = Application
    context_object_name = 'applications'

    def get_queryset(self, *args, **kwargs):
        return Application.objects.filter(is_deleted=False)


class ApplicationAddView(LoginRequiredMixin, AdminPassedTestMixin, CreateView):
    template_name = 'applications/application_add.html'
    model = Application
    form_class = ApplicationSendForm

    def get_success_url(self):
        return reverse('applications_list')
