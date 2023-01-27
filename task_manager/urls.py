from django.contrib import admin
from django.urls import path, include
from .views import IndexView, LoginUserView, LogoutUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginUserView.as_view(), name='login_page'),
    path('logout/', LogoutUserView.as_view(), name='logout_page'),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('tasks/', include('tasks.urls')),
    path('labels/', include('labels.urls')),
]
