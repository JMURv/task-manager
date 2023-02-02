from __future__ import unicode_literals

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
from django.utils.translation import gettext_lazy as _


class UsersView(ListView):
    model = get_user_model()
    template_name = 'users.html'


class UsersCreateView(SuccessMessageMixin, CreateView):
    template_name = 'create.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('login_page')
    success_message = _('User created successfully')


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
    success_message = _('User successfully changed')


class UsersDeleteView(
    AuthRequiredMixin,
    SelfEditPermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'delete.html'
    model = get_user_model()
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().creator.exists() or self.get_object().executor.exists():
            messages.error(
                self.request,
                _("Can't delete, user in use")
            )
            return redirect('status_list')

        return super().post(request, *args, **kwargs)
