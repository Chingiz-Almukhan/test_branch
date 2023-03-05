from django.urls import path

from students.views import (MedicalCertificateCreateView, PaymentCreateView,
                            StudentAddView, StudentDetailView, StudentEditView,
                            StudentListView, student_detail_view,
                            student_groupings_view, student_homeworks_view,
                            student_payments_view, add_student_to_grouping_view,
                            del_student_from_grouping_view)

urlpatterns = [
    path('information/', student_detail_view, name='information'),
    path('payments/', student_payments_view, name='student_payments'),
    path('groupings/', student_groupings_view, name='student_groupings'),
    path('add-student-to-grouping', add_student_to_grouping_view, name='add_student_to_grouping'),
    path('del-student-from-qrouping', del_student_from_grouping_view, name='del_student_from_grouping'),

    path('homeworks/', student_homeworks_view, name='student_homeworks'),

    path('', StudentListView.as_view(), name='students'),

    # TODO данный url не используется, принять решение по нему
    path('add/', StudentAddView.as_view(), name='student_add'),
    path('<int:pk>', StudentDetailView.as_view(), name='student'),
    path('<int:pk>/medical-certificate/create', MedicalCertificateCreateView.as_view(),
         name='medical_certificate_create'),
    path('<int:pk>/payment/create', PaymentCreateView.as_view(), name='payment_create'),
    path('update/<int:pk>', StudentEditView.as_view(), name='student_update'),
]
