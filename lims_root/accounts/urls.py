from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot/', views.user_forgot, name='forgot-password'),
    path('register/', views.user_register, name='register'),
    path('success/', TemplateView.as_view(
        template_name='accounts/register-success.html'),
         name='register-success'),

    path('ajax-update-email/', views.update_email,
         name='ajax-update-email'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
]
