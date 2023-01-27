from django.shortcuts import redirect

from django.urls import reverse_lazy

from task_manager.mixins import AuthRequiredMixin

from .forms import StatusForm
from .models import Status

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class StatusView(AuthRequiredMixin, ListView):
    template_name = 'status_list.html'
    login_url = reverse_lazy('login_page')
    model = Status


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status_create.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно создан'


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'status_update.html'
    model = Status
    form_class = StatusForm
    success_message = 'Статус успешно изменён'
    success_url = reverse_lazy('status_list')


class StatusDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'status_delete.html'
    model = Status
    success_url = reverse_lazy('status_list')
    success_message = 'Статус успешно удалён'

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(
                self.request,
                'Невозможно удалить статус, потому что он используется'
            )
            return redirect('status_list')
        return super().post(request, *args, **kwargs)
