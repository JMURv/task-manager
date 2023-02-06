from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from labels.models import Label
from django.urls import reverse_lazy
from django.shortcuts import redirect
from task_manager.mixins import AuthRequiredMixin
from django.utils.translation import gettext_lazy as _


class LabelListView(AuthRequiredMixin, ListView):
    template_name = 'label_list.html'
    login_url = reverse_lazy('login_page')
    model = Label


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'label_create.html'
    success_url = reverse_lazy('label_list')
    model = Label
    fields = '__all__'
    success_message = _("Label created successfully")


class LabelDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'label_delete.html'
    model = Label
    success_url = reverse_lazy('label_list')
    success_message = _('Label successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.exists():
            messages.error(
                self.request,
                _("Can't delete, label in use")
            )
            return redirect('label_list')

        return super().post(request, *args, **kwargs)


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'label_update.html'
    model = Label
    fields = '__all__'
    success_message = _('Label successfully changed')
    success_url = reverse_lazy('label_list')
