from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from postboard.filters import PostFilter
from postboard.models import Feedback, Post
from .utilits import confirm_code, confirm_mail, accept_mail
from .forms import FunUserCreationForm
from .models import FunUser


class AccountView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.order_by('-time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        feedbacks = []
        for p in self.filterset.qs:
            feedbacks.append(p.feedback_set.all())
        context['filter_feedback'] = feedbacks
        context['title'] = 'Мой аккаунт'
        return context


    def post(self, request, *args, **kwargs):
        d = request.POST.dict()
        key = 0
        for k, i in d.items():
            if i == 'Принять' or i == 'Удалить':
                key = k
        feedback = get_object_or_404(Feedback, id=key)
        key = str(key)
        if request.POST[key] == 'Принять':
            try:
                feedback.is_active = True
                feedback.save()
            except:
                return HttpResponse(""" <center><h1>Ошибка записи</h1>
                <button><a href="">Повторить</a>
                </button></center> """, charset="utf-8")
            try:
                accept_mail(user=request.user, feedback=feedback)
            except:
                print(f'Ошибка отправки email пользователю {feedback.author} о принятии его отклика')
            redirect(request.META.get('HTTP_REFERER'))
        elif request.POST[key] == 'Удалить':
            try:
                return redirect('feedback_delete', key)
            except:
                return HttpResponse(""" <center><h1>Ошибка удаления</h1>
                <button><a href="">Повторить</a>
                </button></center> """, charset="utf-8")
        return redirect('account')


class RegisterView(CreateView):
    model = FunUser
    form_class = FunUserCreationForm
    success_url = reverse_lazy('confirm')
    extra_context = {'title': 'Зарегистрироваться'}

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
@login_required
def confirm_mail_view(request):
    if request.user.is_staff:
        return render(request, 'users/confirm_mail.html', {'name': 'user', 'code': '123456789',})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1>')


# test the view of the accept email
@login_required
def accept_mail_view(request):
    if request.user.is_staff:
        feedback = get_object_or_404(Feedback, pk=3)
        name = request.user.username
        return render(request, 'users/accept_mail.html', {'name': name, 'feedback': feedback,})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1>')


# test the view of the news email
@login_required
def news_mail_view(request):
    if request.user.is_staff:
        posts = Post.objects.filter(author_id=3)
        msg_data = {'name': request.user.username, 'posts': posts}
        return render(request, 'users/news_mail.html', {'msg_data': msg_data, })
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1>')


# test the view of the notify email
@login_required
def notify_mail_view(request):
    if request.user.is_staff:
        feedback = get_object_or_404(Feedback, pk=3)
        name = request.user.username
        return render(request, 'users/notify_mail.html', {'name': name, 'feedback': feedback,})
    else:
        return HttpResponseForbidden('<h1>Доступ запрещён</h1>')
