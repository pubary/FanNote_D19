from django.urls import path

from postboard.views import PostsList, PostDetail, PostCreate, PostEdit, FeedbackDelete

urlpatterns = [
    path('', PostsList.as_view(template_name='postboard/posts.html'), name='posts'),
    path('posts/create', PostCreate.as_view(template_name='postboard/post_edit.html'), name='post_create'),
    path('post-<int:pk>', PostDetail.as_view(template_name='postboard/post.html'), name='post'),
    # path('feedback-<int:pk>/accept/', feedback_accept, name='feedback_accept'),
    path('feedback-<int:pk>/delete/', FeedbackDelete.as_view(), name='feedback_delete'),
    path('post-<int:pk>/edit', PostEdit.as_view(template_name='postboard/post_edit.html'), name='post_edit'),
]
