from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.DashboardView.as_view(), name="dashboard"),

    # Task CRUD
    path("task/new/", views.TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_edit"),
    path("task/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),

    # AJAX / quick actions
    path("task/<int:pk>/toggle/", views.toggle_task_status, name="task_toggle"),
    path("task/quick-add/", views.quick_add_task, name="task_quick_add"),

    # History & stats
    path("history/", views.HistoryView.as_view(), name="history"),
]
