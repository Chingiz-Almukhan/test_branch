from django.views.generic import View, ListView, CreateView, UpdateView
from education.models import ClassTime
from education.forms.class_time_form import ClassTimeForm
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404


class ClassTimeListView(ListView):
    template_name = 'education/class_times.html'
    model = ClassTime
    context_object_name = 'class_time'

    def get_queryset(self, *args, **kwargs):
        return ClassTime.objects.filter(is_deleted=False).order_by('time_start')


class ClassTimeAddView(CreateView):
    template_name = 'education/class_time_add.html'
    form_class = ClassTimeForm
    model = ClassTime

    def get_success_url(self):
        return reverse('class_time')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        time_start = self.request.POST.get('time_start')
        time_end = self.request.POST.get('time_end')
        print('Print', form, '+++', time_start, "+++", time_end )
        if form.is_valid():
            form.save()
            class_time = ClassTime.objects.create(time_start=time_start, time_end=time_end)
            class_time.save()
            return redirect ('class_times')


class ClassTimeEditView(UpdateView):
    template_name = 'education/class_time_update.html'
    model = ClassTime
    form_class = ClassTimeForm
    context_object_name = 'class_time'

    def get_success_url(self):
        return reverse('class_time')


class DelClassTimeView(View):
    def post(self, *args, **kwargs):
        class_time = get_object_or_404(ClassTime, pk=kwargs['pk'])
        class_time.is_deleted = True
        class_time.save()
        return redirect('class_times')
