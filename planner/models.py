from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#6366f1")  # hex
    icon = models.CharField(max_length=10, default="📌")

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("skipped", "Skipped"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_time", "priority"]

    def __str__(self):
        return f"{self.title} ({self.date})"

    @property
    def duration_minutes(self):
        if self.start_time and self.end_time:
            start = datetime.datetime.combine(datetime.date.today(), self.start_time)
            end = datetime.datetime.combine(datetime.date.today(), self.end_time)
            delta = end - start
            return int(delta.total_seconds() / 60)
        return None

    @property
    def priority_color(self):
        return {"low": "#22c55e", "medium": "#f59e0b", "high": "#ef4444"}.get(self.priority, "#6366f1")

    @property
    def is_overdue(self):
        if self.status == "pending" and self.end_time:
            now = timezone.localtime(timezone.now())
            task_end = datetime.datetime.combine(self.date, self.end_time)
            task_end = timezone.make_aware(task_end)
            return now > task_end
        return False


class DailyLog(models.Model):
    """Tracks daily completion for streak system."""
    date = models.DateField(unique=True)
    tasks_total = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    productivity_score = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Log {self.date} — {self.productivity_score:.0f}%"

    @property
    def completion_rate(self):
        if self.tasks_total == 0:
            return 0
        return round((self.tasks_completed / self.tasks_total) * 100)
