from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View

from django.contrib import messages


class StatusView(View):

    def get(self, request):
        statuses = status.objects.all()
        return render(request, 'statuses.html', context={
            'statuses': statuses,
        })


class StatusCreateView(View):

    def get(self, request, *args, **kwargs):
        form = CreateStatusForm()
        return render(request, 'create.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = CreateStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_list')
        return render(request, 'create.html', context={
            'form': form,
        })


class StatusUpdateView(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('status_id')
        status_model = get_status_model()
        status = status_model.objects.get(id=status_id)
        form = CreateStatusForm(instance=status)
        return render(request, 'update.html', {'form': form, 'status_id': status_id})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('status_id')
        status_model = get_status_model()
        status = status_model.objects.get(id=status_id)
        form = CreateStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('users_list')
        return render(request, 'update.html', {'form': form, 'status_id': status_id})


class StatusDeleteView(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('user_id')
        status_model = get_status_model()
        status = status_model.objects.get(id=status_id)
        return render(request, 'delete.html', {'status': status, 'status_id': status_id})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('user_id')
        status_model = get_status_model()
        status = user_model.objects.get(id=status_id)
        if status:
            status.delete()
        return redirect('status_list')
