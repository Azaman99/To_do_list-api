from django.urls import path
from . import views


urlpatterns = [
    path('task/', views.task, name="task"),
    path("tasks/<int:task_id>", views.task_detail),
]
