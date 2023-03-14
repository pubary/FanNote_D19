from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import AccountView, RegisterView, ConfirmView, confirm_mail_view, confirm_mail_error, accept_mail_view

urlpatterns = [
    path('account/', AccountView.as_view(template_name='users/account.html'), name='account'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('confirm-mail-view/', confirm_mail_view, name='confirm_mail'),
    path('confirm-mail-error/', confirm_mail_error, name='confirm_mail_error'),
    path('accept-mail-view/', accept_mail_view, name='accept_mail'),
]
