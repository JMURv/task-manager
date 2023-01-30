from .models import Task
from .filters import TaskFilter

from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, TaskDeletePermissionMixin


class TasksListView(AuthRequiredMixin, FilterView):
    template_name = 'task_list.html'
    model = Task
    filterset_class = TaskFilter


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'task_create.html'
    model = Task
    success_message = 'Задача успешно создана'
    success_url = reverse_lazy('list_task')
    fields = ['name', 'description', 'status', 'executor', 'labels']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'task_update.html'
    model = Task
    fields = ['name', 'description', 'executor', 'status', 'labels']
    success_url = reverse_lazy('list_task')
    success_message = 'Задача успешно изменена'


class TaskDeleteView(
    AuthRequiredMixin,
    TaskDeletePermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'task_delete.html'
    model = Task
    success_url = reverse_lazy('list_task')
    success_message = 'Задача успешно удалена'


class TaskDetailView(AuthRequiredMixin, DetailView):
    template_name = 'task_detail.html'
    model = Task
