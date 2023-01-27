from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from labels.models import Label
from django.urls import reverse_lazy
from django.shortcuts import redirect
from manager.mixins import AuthRequiredMixin


class LabelListView(AuthRequiredMixin, ListView):
    template_name = 'label_list.html'
    login_url = reverse_lazy('login_page')
    model = Label


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'label_create.html'
    success_url = reverse_lazy('label_list')
    model = Label
    fields = '__all__'
    success_message = 'Метка успешно создана'


class LabelDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'label_delete.html'
    model = Label
    success_url = reverse_lazy('label_list')
    success_message = 'Метка успешно удалена'

    def post(self, request, *args, **kwargs):
        if self.get_object().task_set.all():
            messages.error(
                self.request,
                'Невозможно удалить метку, потому что она используется'
            )
            return redirect('label_list')

        return super().post(request, *args, **kwargs)


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'label_update.html'
    model = Label
    fields = '__all__'
    success_message = 'Метка успешно изменена'
    success_url = reverse_lazy('label_list')
