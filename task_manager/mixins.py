from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class AuthRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(
            self.request,
            _('You are not authorized!')
        )
        return super().handle_no_permission()


class TaskDeletePermissionMixin(UserPassesTestMixin):

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.error(
                self.request,
                _("You can't delete this task. Only author can"))
            return redirect(reverse_lazy('list_task'))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        self.object = self.get_object()
        return self.object.creator == self.request.user


class SelfEditPermissionMixin(UserPassesTestMixin):

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.test_func()
        if not user_test_result:
            messages.error(self.request, _("You have't permission!"))
            return redirect(reverse_lazy('users_list'))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        self.object = self.get_object()
        return self.object == self.request.user
