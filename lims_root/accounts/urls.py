from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot/', views.forgot_view, name='forgot-password'),
    path('register/', views.register_view, name='register'),
    path('success/', TemplateView.as_view(
        template_name='accounts/register-success.html'),
         name='register-success'),

    path('home/', views.user_home, name='user-home'),
]
