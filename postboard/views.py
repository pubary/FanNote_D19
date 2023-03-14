from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from postboard.forms import PostForm
from postboard.models import Post, Feedback
from postboard.utilits import send_feedback


class PostsList(ListView):
    model = Post
    ordering = '-time'
    context_object_name = 'posts'
    paginate_by = 8
    extra_context = {'title': 'Наши объявления'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity'] = Post.objects.all().count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback.objects.filter(post_id=self.kwargs['pk'])#, is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            post_pk = kwargs['pk']
            post = get_object_or_404(Post, id=post_pk)
            try:
                send_feedback(request, post)
            except:
                return HttpResponse(""" <center><h1>Ошибка отправки</h1>
                <button><a href="">Повторить</a>
                </button></center> """, charset="utf-8")
            return redirect('post', kwargs['pk'])
        return redirect('post', kwargs['pk'])


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    extra_context = {'title': 'Создать объявление', }

    def form_valid(self, form, **kwargs):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    extra_context = {'title': 'Редактировать объявление', }

    def get(self, request, *args, **kwargs):
        author = get_object_or_404(Post, pk=self.kwargs['pk']).author
        if author != self.request.user:
            return HttpResponseForbidden("""<center><h2>Доступ заблокирован!</h2>
             <h4>Вы не являетесь автором этого объявления!</h4>
             <button><a href="/">Назад</a></button></center>'""")
        else:
            return super().get(self, request, *args, **kwargs)


class FeedbackDelete(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'postboard/feedback_delete.html'
    success_url = reverse_lazy('account')
    extra_context = {'title': 'Удаление отклика'}
