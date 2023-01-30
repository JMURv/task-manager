import django_filters
from .models import Task
from labels.models import Label
from django import forms


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method='filter_self_tasks',
        label='Только свои задачи'
    )

    label = django_filters.filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label='Метка'
    )

    def filter_self_tasks(self, queryset, smth, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
