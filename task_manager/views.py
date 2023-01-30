from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = 'Вы залогинены!'
    redirect_authenticated_user = reverse_lazy('index')
    success_url = reverse_lazy('index')


class LogoutUserView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
