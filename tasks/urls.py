from django.urls import path
from . import views





urlpatterns = [
    
    path('tasks/',views.tasks,name='tasks'),
    path('popup/',views.popup,name='popup'),
]
