from django.urls import path
from .views import IndexView, LoginUser, LogoutView, \
    UsersView, UsersCreateView, UsersUpdateView, UsersDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),
    path('users/', UsersView.as_view(), name='users_list'),
    path('users/create', UsersCreateView.as_view(), name='create_user'),
    path('users/<int:user_id>/update/', UsersUpdateView.as_view(), name='update_user'),
    path('users/<int:user_id>/delete/', UsersDeleteView.as_view(), name='delete_user'),

]
