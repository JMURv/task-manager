from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class AuthRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('You are not authorized!')
        self.permission_denied_url = reverse_lazy('login_page')
        if not request.user.is_authenticated:
            messages.error(
                request,
                messages.error(self.request, self.permission_denied_message)
            )
            return redirect('login_page')
        return super().dispatch(request, *args, **kwargs)


class TaskDeletePermissionMixin:
    def get(self, request, *args, **kwargs):
        self.permission_denied_message = _("You can't delete this task. Only author can")
        self.permission_denied_url = reverse_lazy('list_task')
        self.object = self.get_object()

        if self.object.creator == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)


class SelfEditPermissionMixin:
    def get(self, request, *args, **kwargs):
        self.permission_denied_message = _("You have't permission!")
        self.permission_denied_url = reverse_lazy('users_list')
        self.object = self.get_object()

        if self.object == self.request.user:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(self.request, self.permission_denied_message)
            return redirect(self.permission_denied_url)
