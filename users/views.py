from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from .utilits import confirm_code, confirm_mail
from .forms import FunUserCreationForm
from .models import FunUser


class AccountView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой аккаунт'
        return context


class RegisterView(CreateView):
    model = FunUser
    form_class = FunUserCreationForm
    success_url = reverse_lazy('confirm')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.code = confirm_code()
        try:
            confirm_mail(user)
        except:
            return redirect('confirm_mail_error')
        else:
            return super().form_valid(form)


class ConfirmView(View):

    def get(self, request, *args, **kwargs):
        context = {'title': 'Подтверждение регистрации'}
        return render(request, 'users/confirm.html', context)

    def post(self, request, *args, **kwargs):
        if request.POST:
            username = request.POST['username']
            code = request.POST['code']
            try:
                user = FunUser.objects.get(username=username)
                if code == user.code:
                    user.is_active = True
                    user.save()
            except:
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('account')


def confirm_mail_error(request):
    return render(request, 'users/confirm_mail_error.html')


# test the view of the confirm email
def confirm_mail_view(request):
    return render(request, 'users/confirm_mail.html', {'name': 'user', 'code': '123456789',})


