

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('create/', views.create_command),
    path('open-existing/', views.open_existing_port),
    path('get-latest-command/', views.get_latest_command),
    path('sessions/', views.list_all_sessions),
    path('manage/', views.manage_sessions, name='manage_sessions'),
]



