from django.urls import path
from .views import StatusView, StatusCreateView, \
    StatusUpdateView, StatusDeleteView

urlpatterns = [
    path('', StatusView.as_view(), name='status_list'),
    path('create', StatusCreateView.as_view(), name='create_status'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='update_status'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='delete_status'),

]
