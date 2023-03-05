from django.urls import path

from education.views.base import IndexView
from education.views.class_time import (ClassTimeAddView, ClassTimeEditView,
                                        ClassTimeListView, DelClassTimeView)
from education.views.contracts import open_contract_pdf, send_contract
from education.views.discounts import (DelDiscountView, DiscountAddView,
                                       DiscountEditView, DiscountListView)
from education.views.groupings import (DelGroupingView, GroupingAddView,
                                       GroupingEditView, GroupingListView,
                                       add_teacher_to_grouping_view,
                                       remove_teacher_from_grouping_view)
from education.views.packages import (DelPackageView, PackageAddView,
                                      PackageEditView, PackageListView)
from education.views.schedule import (ScheduleCreateView,
                                      get_student_groupings_view,
                                      get_teacher_groupings_view,
                                      schedule_generate_view,
                                      set_schedule_not_active)
from education.views.schedule_download_view import schedule_download
from education.views.subjects import (DelSubjectView, SubjectAddView,
                                      SubjectEditView, SubjectListView)
from education.views.teachers import (TeacherDetailView, TeacherEditView,
                                      TeachersListView)
from lessons.views import CalendarView

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('crm/', CalendarView.as_view(), name='crm'),

    path('schedule-create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule-generate/', schedule_generate_view, name='schedule_generate'),
    path('schedule-clear/', set_schedule_not_active, name='schedule_clear'),
    path('schedule/student/<int:student_pk>/groupings/', get_student_groupings_view, name='student_groupings'),
    path('schedule/teacher/<int:teacher_pk>/groupings/', get_teacher_groupings_view, name='teacher_groupings'),
    path('export/schedule', schedule_download, name='export_schedule'),

    path('subjects/', SubjectListView.as_view(), name='subjects'),
    path('subject_add/', SubjectAddView.as_view(), name='subject_add'),
    path('subject_update/<int:pk>', SubjectEditView.as_view(), name='subject_update'),
    path('subject_del/<int:pk>', DelSubjectView.as_view(), name='subject_del'),

    path('packages/', PackageListView.as_view(), name='packages'),
    path('package_add/', PackageAddView.as_view(), name='package_add'),
    path('package_update/<int:pk>', PackageEditView.as_view(), name='package_update'),
    path('package_del/<int:pk>', DelPackageView.as_view(), name='package_del'),
    path('discounts/', DiscountListView.as_view(), name='discounts'),
    path('discount_add/', DiscountAddView.as_view(), name='discount_add'),
    path('discount_update/<int:pk>', DiscountEditView.as_view(), name='discount_update'),
    path('discount_del/<int:pk>', DelDiscountView.as_view(), name='discount_del'),

    path('groupings/', GroupingListView.as_view(), name='groupings'),
    path('groupings/remove-teacher/<int:pk>', remove_teacher_from_grouping_view, name='remove_teacher_from_grouping'),
    path('groupings/add-teacher/', add_teacher_to_grouping_view, name='add_teacher_to_grouping'),
    path('grouping_add/', GroupingAddView.as_view(), name='grouping_add'),
    path('grouping_update/<int:pk>', GroupingEditView.as_view(), name='grouping_update'),
    path('grouping_del/<int:pk>', DelGroupingView.as_view(), name='grouping_del'),


    path('open_contract/<int:pk>', open_contract_pdf, name='open_contract'),
    path('send_contract/<int:pk>', send_contract, name='send_contract'),

    path('times/', ClassTimeListView.as_view(), name='class_times'),
    path('time_add/', ClassTimeAddView.as_view(), name='class_time_add'),
    path('time_update/<int:pk>', ClassTimeEditView.as_view(), name='class_time_update'),
    path('time_del/<int:pk>', DelClassTimeView.as_view(), name='class_time_del'),

    path('teachers/', TeachersListView.as_view(), name='teachers'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='teacher'),
    path('teacher_update/<int:pk>', TeacherEditView.as_view(), name='teacher_update'),
]
