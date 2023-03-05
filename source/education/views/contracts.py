import datetime
import tempfile

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from weasyprint import CSS, HTML

from applications.models import Application

MONTH = [
    "Қантар",
    "Ақпан",
    "Наурыз",
    "Сәуір",
    "Мамыр",
    "Маусым",
    "Шілде",
    "Тамыз",
    "Қыркүйек",
    "Қазан",
    "Қараша",
    "Желтоксан",
]


@login_required
def render_pdf(request, application):
    """Формирование PDF Файла"""
    cur_date = datetime.datetime.now()
    application.contract_date = cur_date
    application.save()
    month = MONTH[cur_date.month - 1]
    html_string = render_to_string('education/contract_template.html',
                                   {'app': application,
                                    'date': cur_date,
                                    'month': month,
                                    },
                                   )
    css = CSS(string=''' @page {size: 220mm 297mm;}''')
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf(stylesheets=[css])
    return result


@login_required
def open_contract_pdf(request, *args, **kwargs):
    application = Application.objects.get(pk=kwargs.get('pk'))
    contract = render_pdf(request, application)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=contract.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(contract)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response


@login_required
def send_contract(request, *args, **kwargs):
    app = Application.objects.get(pk=kwargs.get('pk'))
    contract = render_pdf(request, app)
    emails = [app.email, app.parents_email]
    for email in emails:
        email_msg = EmailMessage('Договор', body=contract, from_email='testeruly@yandex.kz', to=[email])
        email_msg.attach('contract.pdf', contract, "application/pdf")
        email_msg.content_subtype = "pdf"
        email_msg.encoding = 'UTF-8'
        email_msg.send()
    response = {'answer': _('Договор отправлен')}
    return JsonResponse(response)
