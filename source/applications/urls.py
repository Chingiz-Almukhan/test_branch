from django.urls import path

from applications.views import (ApplicationAddView,
                                ApplicationDetailView, ApplicationEditView,
                                ApplicationRejectView, ApplicationsListView,
                                DeleteApplicationView)

urlpatterns = [
    path('update/<int:pk>', ApplicationEditView.as_view(), name='application_update'),
    path('reject/<int:pk>', ApplicationRejectView.as_view(), name='application_reject'),

    path('delete/<int:pk>', DeleteApplicationView.as_view(), name='application_delete'),
    path('detail/<int:pk>', ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/', ApplicationsListView.as_view(), name='applications_list'),
    path('application_add/', ApplicationAddView.as_view(), name='application_add')
]
