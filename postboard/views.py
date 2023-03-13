from django.views.generic import ListView, DetailView

from postboard.models import Post


class PostsList(ListView):
    model = Post
    ordering = '-time'

    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['quantity'] = Post.objects.all().count()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'