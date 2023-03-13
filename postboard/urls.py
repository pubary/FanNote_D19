from django.urls import path

from postboard.views import PostsList, PostDetail


urlpatterns = [
    path('', PostsList.as_view(template_name='postboard/posts.html'), name='posts'),
    path('<int:pk>', PostDetail.as_view(template_name='postboard/post.html'), name='post_detail'),
]