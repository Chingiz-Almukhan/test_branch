import datetime
import tempfile

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from education.models import Auditorium


def schedule_download(request):
    auditoriums = Auditorium.objects.all()
    sum_dict = {'108': {}, '109': {}, '110': {}}
    for auditorium in auditoriums:
        schedules = auditorium.schedules.filter(is_deleted=False)
        my_dict = {'monday': {}, 'tuesday': {}, 'wednesday': {}, 'thursday': {}, 'friday': {}, 'saturday': {}}
        for schedule in schedules:
            my_dict[schedule.week_day][schedule.class_time.number_lesson] = schedule.grouping.name
        sum_dict[auditorium.name] = my_dict

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Schedule-' + \
                                      str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string('education/schedule_pdf.html',
                                   {'sum_dict': sum_dict})
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
