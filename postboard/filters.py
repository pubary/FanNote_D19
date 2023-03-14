from django.forms import DateInput, RadioSelect
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter, ModelChoiceFilter, ChoiceFilter

from postboard.models import Post


# class FeedbackFilter(FilterSet):
#     post = ModelMultipleChoiceFilter(
#         field_name='post__title',
#         queryset=Post.objects.filter(author='user'),
#         label='Категория (или одна или несколько)',
#         conjoined=True,
#     )
#     time = DateTimeFilter(
#         field_name='time',
#         lookup_expr='gte',
#         widget=DateInput(attrs={'type': 'date'}),
#     )
#     # author = ModelChoiceFilter(
#     #     field_name='author__author_acc',
#     #     queryset=Author.objects.all(),
#     #     label='Автор',
#     # )
#
#     class Meta:
#         model = Post
#         fields = {
#             'title': ['icontains'],
#             'text': ['icontains'],
# #            'p_type': ['exact'],
#             }


