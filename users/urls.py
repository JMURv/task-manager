from django.urls import path
from .views import UsersView, UsersCreateView, UsersUpdateView, UsersDeleteView

urlpatterns = [
    path('', UsersView.as_view(), name='users_list'),
    path('create/', UsersCreateView.as_view(), name='create_user'),
    path('<int:pk>/update/', UsersUpdateView.as_view(), name='update_user'),
    path('<int:pk>/delete/', UsersDeleteView.as_view(), name='delete_user'),
]
