from django.forms import DateInput, TextInput
from django_filters import FilterSet, DateTimeFilter, Filter


class PostFilter(FilterSet):
    title = Filter(
        field_name='title',
        lookup_expr='icontains',
        label='заголовок, которых содержит',
        widget=TextInput(attrs={'cols': 120})
    )
    time = DateTimeFilter(
        field_name='time',
        lookup_expr='gte',
        label='и дата написания этих объявлений (не раньше)',
        widget=DateInput(attrs={'type': 'date'}),
    )


