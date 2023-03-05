from django.urls import path

from lessons.views import (CalendarView, LessonDetailView, lesson_edit_view,
                           lessons_generate_view,
                           update_teacher_in_lesson_view)

urlpatterns = [
    path('', CalendarView.as_view(), name='calendar'),
    path('<int:pk>', LessonDetailView.as_view(), name='lesson-detail'),
    path('edit/<int:lesson_pk>', lesson_edit_view, name='lesson-edit'),
    path('update-teacher/', update_teacher_in_lesson_view, name='lesson-update-teacher'),
    path('generate/', lessons_generate_view, name='lessons_generate'),
]
