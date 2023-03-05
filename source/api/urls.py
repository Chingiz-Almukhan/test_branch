from django.urls import path, include

from api.views.application_first_form import SaveApplication, SaveApplicantContract, SaveApplicationPayedInfo
from api.views.check_user import CheckUser
from api.views.create_application_view import AddApplicationView
from api.views.create_student_by_application_view import CreateStudent
from api.views.get_schedule_view import all_lessons
from api.views.sum_package_view import SumPackageView, SumDiscountView

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_sum', SumPackageView.as_view(), name='sum_package'),
    path('get_discount', SumDiscountView.as_view(), name='sum_discount'),
    path('create-application/', AddApplicationView.as_view({'post': 'create'}), name='add_application_api'),
    path('create-student-by-application/<int:pk>', CreateStudent.as_view(), name='Create_student_by_application'),
    path('all-lessons', all_lessons, name='all_lessons'),
    path('save-applicant-form-first/<int:pk>', SaveApplication.as_view({'post': 'update'}),
         name='save_first_form_for_application'),
    path('save-applicant-contract/<int:pk>', SaveApplicantContract.as_view({'post': 'update'}),
         name='save_applicant_contract'),
    path('application-payed/<int:pk>', SaveApplicationPayedInfo.as_view({'post': 'update'}),
         name='save_application-payed_info'),
    path('check_user', CheckUser.as_view(), name='check_user')
]
