from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views import View

from django.contrib.auth import get_user_model

from manager.forms import CreateUserForm


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class UsersView(View):

    def get(self, request):
        user = get_user_model()
        users = user.objects.all()
        return render(request, 'users.html', context={
            'users': users,
        })


class UsersCreateView(View):

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, 'create.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
        return render(request, 'create.html', context={
            'form': form,
        })


class UsersUpdateView(View):

    def get(self, request, *args, **kwargs):
        """Страница редактирования"""
        user_id = kwargs.get('user_id')
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        form = CreateUserForm(instance=user)
        return render(request, 'update.html', {'form': form, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        """Обновление"""
        user_id = kwargs.get('user_id')
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
        return render(request, 'update.html', {'form': form, 'user_id': user_id})


class UsersDeleteView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        return render(request, 'delete.html', {'user': user, 'user_id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user_model = get_user_model()
        user = user_model.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users_list')


class LoginView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'login.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users_list')


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect('users_list')
