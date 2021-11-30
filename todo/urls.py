from django.urls import path
from . import views


urlpatterns = [
    path('task/', views.task, name="task"),
    path("tasks/<int:task_id>", views.task_detail),
    path('todos/mark_complete/<int:todo_id>', views.mark_complete),
    path('todos/today/', views.today_list),
    path('todos/anydate/', views.future_list),
]
