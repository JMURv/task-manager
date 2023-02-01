from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.mixins import AuthRequiredMixin
from .forms import StatusForm
from .models import Status
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _


class StatusView(AuthRequiredMixin, ListView):
    template_name = 'status_list.html'
    login_url = reverse_lazy('login_page')
    model = Status


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'status_create.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('status_list')
    success_message = _("Status created successfully")


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'status_update.html'
    model = Status
    form_class = StatusForm
    success_message = _('Status successfully changed')
    success_url = reverse_lazy('status_list')


class StatusDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'status_delete.html'
    model = Status
    success_url = reverse_lazy('status_list')
    success_message = _('Status successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(
                self.request,
                _("Can't delete, status in use")
            )
            return redirect('status_list')
        return super().post(request, *args, **kwargs)
