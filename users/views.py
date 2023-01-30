from task_manager.mixins import SelfEditPermissionMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from users.forms import UserForm
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.mixins import AuthRequiredMixin


class UsersView(ListView):
    model = get_user_model()
    template_name = 'users.html'


class UsersCreateView(SuccessMessageMixin, CreateView):
    template_name = 'create.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('login_page')
    success_message = 'Пользователь успешно зарегистрирован'


class UsersUpdateView(
    AuthRequiredMixin,
    SelfEditPermissionMixin,
    SuccessMessageMixin,
    UpdateView
):
    template_name = 'update.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменён'


class UsersDeleteView(
    SelfEditPermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'delete.html'
    model = get_user_model()
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удалён'

    def post(self, request, *args, **kwargs):
        if self.get_object().creator.all() or self.get_object().executor.all():
            messages.error(
                self.request,
                'Невозможно удалить пользователя, потому что он используется'
            )
            return redirect('status_list')

        return super().post(request, *args, **kwargs)
