from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from postboard.models import Feedback
from .utilits import confirm_code, confirm_mail
from .forms import FunUserCreationForm
from .models import FunUser


class AccountView(LoginRequiredMixin, ListView):
    model = Feedback
    ordering = '-time'
    context_object_name = 'feedbacks'
    paginate_by = 5

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = FeedbackFilter(self.request.GET, queryset)
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filterset'] = self.filterset
        context['title'] = 'Мой аккаунт'
        return context

    def post(self, request, *args, **kwargs):
        key = list(dict(request.POST.lists()).keys())[0]
        feedback = get_object_or_404(Feedback, id=key)
        if request.POST['key'] == 'save':
            try:
                feedback.is_active = True
                feedback.save()
            except:
                return HttpResponse(""" <center><h1>Ошибка записи</h1>
                <button><a href="">Повторить</a>
                </button></center> """, charset="utf-8")
            return redirect(request.META.get('HTTP_REFERER'))
        elif request.POST['key'] == 'delete':
            try:
                feedback.delete()
            except:
                return HttpResponse(""" <center><h1>Ошибка удаления</h1>
                <button><a href="">Повторить</a>
                </button></center> """, charset="utf-8")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect(request.META.get('HTTP_REFERER'))


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
            content = """<center><h1>Ошибка ввода</h1><button><a href="">Повторить</a></button></center>"""
            try:
                user = FunUser.objects.get(username=username)
                if code == user.code:
                    user.is_active = True
                    user.save()
                    return redirect('account')
                else:
                    return HttpResponse(content, charset="utf-8")
            except:
                return HttpResponse(content, charset="utf-8")
        return redirect(request.META.get('HTTP_REFERER'))


def confirm_mail_error(request):
    return render(request, 'users/confirm_mail_error.html')


# test the view of the confirm email
def confirm_mail_view(request):
    return render(request, 'users/confirm_mail.html', {'name': 'user', 'code': '123456789',})


