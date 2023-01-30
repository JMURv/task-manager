from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AuthRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = 'Вы не авторизованы!'
        self.permission_denied_url = reverse_lazy('login_page')
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class TaskDeletePermissionMixin:
    def get(self, request, *args, **kwargs):
        self.permission_denied_message = 'Задачу может удалить только её автор'
        self.permission_denied_url = reverse_lazy('list_task')
        self.object = self.get_object()

        if self.object.creator == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)


class SelfEditPermissionMixin:
    def get(self, request, *args, **kwargs):
        self.permission_denied_message = 'У вас нет прав для изменения другого пользователя.'
        self.permission_denied_url = reverse_lazy('users_list')
        self.object = self.get_object()

        if self.object == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)
