from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

from api.views.application_first_form import IsSuperUserOrAdmin
from education.models import Schedule


@api_view(['GET'])
@permission_classes([IsSuperUserOrAdmin, ])
def all_lessons(request):
    schedules = Schedule.objects.filter(is_deleted=False)
    out = []
    days_of_week = {'monday': '1', 'tuesday': '2', 'wednesday': '3', 'thursday': '4', 'friday': '5', 'saturday': '6',
                    'sunday': '7'}
    for schedule in schedules:
        group = model_to_dict(schedule.grouping)
        auditorium = model_to_dict(schedule.auditorium)
        out.append({
            'title': f'группа {group["name"]} | аудитория {auditorium["name"]}',
            'daysOfWeek': days_of_week[schedule.week_day],
            'id': schedule.pk,
            'groupId': group["id"],
            'startTime': schedule.class_time.time_start,
            'endTime': schedule.class_time.time_end,
            'startRecur': group['start_date'].date(),
            'endRecur': group['end_date'].date(),
            'backgroundColor': 'red',
        })
    return JsonResponse(out, safe=False)
