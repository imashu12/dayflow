from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q
import datetime
import json

from .models import Task, Category, DailyLog
from .forms import TaskForm, QuickTaskForm


# ─── Helpers ────────────────────────────────────────────────────────────────

def get_or_create_daily_log(date):
    tasks = Task.objects.filter(date=date)
    total = tasks.count()
    completed = tasks.filter(status="completed").count()
    score = calculate_productivity_score(tasks)
    log, _ = DailyLog.objects.update_or_create(
        date=date,
        defaults={"tasks_total": total, "tasks_completed": completed, "productivity_score": score},
    )
    return log


def calculate_productivity_score(tasks):
    if not tasks.exists():
        return 0
    total = tasks.count()
    completed = tasks.filter(status="completed").count()
    high_done = tasks.filter(status="completed", priority="high").count()
    high_total = tasks.filter(priority="high").count()
    base = (completed / total) * 70
    bonus = (high_done / high_total * 30) if high_total else 0
    return round(base + bonus, 1)


def get_streak():
    today = datetime.date.today()
    streak = 0
    current = today - datetime.timedelta(days=1)
    while True:
        try:
            log = DailyLog.objects.get(date=current)
            if log.completion_rate >= 50:
                streak += 1
                current -= datetime.timedelta(days=1)
            else:
                break
        except DailyLog.DoesNotExist:
            break
    return streak


def get_free_slots(tasks, date):
    """Return list of free time windows for smart suggestions."""
    work_start = datetime.time(8, 0)
    work_end = datetime.time(22, 0)
    busy = []
    for t in tasks:
        if t.start_time and t.end_time:
            busy.append((t.start_time, t.end_time))
    busy.sort()
    free = []
    cursor = work_start
    for s, e in busy:
        if cursor < s:
            start_dt = datetime.datetime.combine(date, cursor)
            end_dt = datetime.datetime.combine(date, s)
            mins = int((end_dt - start_dt).total_seconds() / 60)
            if mins >= 15:
                free.append({"start": cursor.strftime("%H:%M"), "end": s.strftime("%H:%M"), "minutes": mins})
        cursor = max(cursor, e)
    if cursor < work_end:
        start_dt = datetime.datetime.combine(date, cursor)
        end_dt = datetime.datetime.combine(date, work_end)
        mins = int((end_dt - start_dt).total_seconds() / 60)
        if mins >= 15:
            free.append({"start": cursor.strftime("%H:%M"), "end": work_end.strftime("%H:%M"), "minutes": mins})
    return free[:3]


# ─── Dashboard ──────────────────────────────────────────────────────────────

class DashboardView(View):
    template_name = "planner/dashboard.html"

    def get(self, request):
        date_str = request.GET.get("date")
        if date_str:
            try:
                selected_date = datetime.date.fromisoformat(date_str)
            except ValueError:
                selected_date = datetime.date.today()
        else:
            selected_date = datetime.date.today()

        tasks = Task.objects.filter(date=selected_date).select_related("category").order_by("start_time", "priority")
        total = tasks.count()
        completed = tasks.filter(status="completed").count()
        progress = round((completed / total) * 100) if total else 0
        log = get_or_create_daily_log(selected_date)
        streak = get_streak()
        free_slots = get_free_slots(tasks, selected_date)
        quick_form = QuickTaskForm(initial={"date": selected_date})
        categories = Category.objects.all()

        # Build timeline hours (6am – 11pm)
        hours = list(range(6, 23))

        # Next/prev day
        prev_date = selected_date - datetime.timedelta(days=1)
        next_date = selected_date + datetime.timedelta(days=1)

        context = {
            "tasks": tasks,
            "selected_date": selected_date,
            "today": datetime.date.today(),
            "total": total,
            "completed": completed,
            "progress": progress,
            "log": log,
            "streak": streak,
            "free_slots": free_slots,
            "quick_form": quick_form,
            "categories": categories,
            "hours": hours,
            "prev_date": prev_date,
            "next_date": next_date,
            "task_form": TaskForm(initial={"date": selected_date}),
        }
        return render(request, self.template_name, context)


# ─── Task CRUD ───────────────────────────────────────────────────────────────

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "planner/task_form.html"

    def get_success_url(self):
        date = self.object.date
        return reverse("dashboard") + f"?date={date}"

    def form_valid(self, form):
        messages.success(self.request, "Task added successfully! 🎯")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below.")
        return super().form_invalid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "planner/task_form.html"

    def get_success_url(self):
        date = self.object.date
        return reverse("dashboard") + f"?date={date}"

    def form_valid(self, form):
        messages.success(self.request, "Task updated! ✅")
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "planner/task_confirm_delete.html"

    def get_success_url(self):
        date = self.object.date
        return reverse("dashboard") + f"?date={date}"

    def form_valid(self, form):
        messages.success(self.request, "Task deleted.")
        return super().form_valid(form)


# ─── AJAX / Quick Actions ────────────────────────────────────────────────────

@require_POST
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = json.loads(request.body)
    new_status = data.get("status", "completed")
    task.status = new_status
    task.save()
    get_or_create_daily_log(task.date)
    return JsonResponse({"status": task.status, "ok": True})


@require_POST
def quick_add_task(request):
    date_str = request.POST.get("date", str(datetime.date.today()))
    try:
        date = datetime.date.fromisoformat(date_str)
    except ValueError:
        date = datetime.date.today()

    form = QuickTaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.date = date
        task.save()
        get_or_create_daily_log(date)
        messages.success(request, "Quick task added! ⚡")
    else:
        messages.error(request, "Could not add task. Check the fields.")
    return redirect(reverse("dashboard") + f"?date={date}")


# ─── Stats / History ─────────────────────────────────────────────────────────

class HistoryView(ListView):
    model = DailyLog
    template_name = "planner/history.html"
    context_object_name = "logs"
    paginate_by = 14

    def get_queryset(self):
        return DailyLog.objects.order_by("-date")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["streak"] = get_streak()
        # Last 7 days for mini chart
        today = datetime.date.today()
        week = []
        for i in range(6, -1, -1):
            d = today - datetime.timedelta(days=i)
            try:
                log = DailyLog.objects.get(date=d)
                week.append({"date": d.strftime("%a"), "score": log.productivity_score})
            except DailyLog.DoesNotExist:
                week.append({"date": d.strftime("%a"), "score": 0})
        ctx["week_data"] = json.dumps(week)
        return ctx
