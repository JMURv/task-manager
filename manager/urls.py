from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('users/', views.UsersView.as_view(), name='users_list'),
    path('users/create', views.UsersCreateView.as_view(), name='create_user'),
    path('users/<int:user_id>/update/', views.UsersUpdateView.as_view(), name='update_user'),
    path('users/<int:user_id>/delete/', views.UsersDeleteView.as_view(), name='delete_user'),

]
