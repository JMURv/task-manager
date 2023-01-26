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
