from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from accounts.views.login_view import LoginView
from accounts.views.logout_view import logout_view
from accounts.views.profile_view import ProfileView
from accounts.views.register_view import RegisterView

urlpatterns = [
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('register/<str:pk>', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-change/', PasswordChangeView.as_view(template_name="password_change_form.html"),
         name='password_change'),
    path('password-change/done/', logout_view, name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(template_name="password_reset_form.html"), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete'),

    path('password-change/', PasswordChangeView.as_view(template_name="password_change_form.html"),
         name='password_change'),
    path('password-change/done/', logout_view, name='password_change_done'),
]
