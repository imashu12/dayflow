from django.contrib import admin
from .models import Task, Category, DailyLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "icon"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "start_time", "end_time", "priority", "status", "category"]
    list_filter = ["date", "priority", "status", "category"]
    search_fields = ["title", "description"]
    date_hierarchy = "date"


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ["date", "tasks_total", "tasks_completed", "productivity_score"]
