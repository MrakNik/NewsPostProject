from django.forms import DateInput
from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter

from .models import Post, Category


class PostFilter(FilterSet):
    post = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        conjoined=False,
    )

    time_in = DateFilter(

        lookup_expr='lt',
        widget=DateInput(attrs={'placeholder': 'Select a date', 'type': 'date'}),
        label='Date',

    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'position': ['icontains'],

        }
