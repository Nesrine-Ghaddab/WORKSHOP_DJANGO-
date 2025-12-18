from django.urls import path
from . import views
urlpatterns = [
 path('info/', views.get_agent_card, name='agent_info'),

 path('tasks/',views.handle_task, name='agent_tasks'),
 path('interface/',views.interface_client, name='template'),
]