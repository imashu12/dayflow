<<<<<<< HEAD
# ⚡ DayFlow — Production-Ready Daily Planner

A startup-level daily planner built with Django. Clean dark UI, timeline view, productivity scoring, streak system, and smart free-slot detection.

---

## 🚀 Quick Start (3 commands)

```bash
pip install django
python setup.py        # migrations + seed data
python manage.py runserver
```

Open **http://127.0.0.1:8000** — you'll see a fully populated dashboard.

---

## 📁 Project Structure

```
dayflow/
├── manage.py
├── setup.py                    # One-time setup & seed script
├── requirements.txt
│
├── dayflow/                    # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── planner/                    # Main application
    ├── models.py               # Task, Category, DailyLog
    ├── views.py                # All CBVs + AJAX endpoints
    ├── forms.py                # TaskForm, QuickTaskForm
    ├── urls.py                 # Clean URL patterns
    ├── admin.py                # Admin registrations
    ├── apps.py
    ├── migrations/
    │   └── 0001_initial.py
    ├── templatetags/
    │   └── planner_tags.py     # Custom template filters
    └── templates/planner/
        ├── base.html           # Layout, sidebar, theme
        ├── dashboard.html      # Main dashboard
        ├── task_form.html      # Add / Edit task
        ├── task_confirm_delete.html
        └── history.html        # Stats & history
```

---

## ✨ Features

### Dashboard
- **Timeline view** — 6am–11pm hourly grid with tasks plotted by start time
- **Live time needle** — animated indicator showing current time (auto-scrolls)
- **Progress bar** — updates instantly via AJAX without page reload
- **Productivity score** — weighted algorithm (base: completion rate, bonus: high-priority tasks done)
- **Streak counter** — counts consecutive days with ≥50% completion
- **Free slot detection** — shows open windows in your schedule, click to prefill the modal

### Task Management
- **Quick Add modal** — ⚡ lightning-fast, stays on page, auto-focuses title
- **Full task form** — title, description, date, time range, priority, category, status
- **Live duration preview** — shows "2h 30m" as you fill in times
- **One-click toggle** — check/uncheck tasks without reloading
- **Priority-coded visuals** — 🔴 High / 🟡 Medium / 🟢 Low with color badges
- **Overdue detection** — red warning on pending tasks past their end time
- **Filter tabs** — All / Pending / Done / Urgent

### History & Analytics
- **7-day bar chart** — color-coded by productivity score
- **Daily log table** — paginated, with completion rate mini-charts
- **One-click navigation** — jump from history to any day's dashboard

### UX
- **Dark/Light mode** — toggle persisted to localStorage
- **Responsive** — hamburger sidebar on mobile
- **Toast notifications** — non-blocking feedback on actions
- **Smooth animations** — fade-up cards, modal transitions

---

## 🧱 Models

### `Task`
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | Required |
| description | TextField | Optional |
| date | DateField | Defaults to today |
| start_time | TimeField | Optional, used for timeline |
| end_time | TimeField | Optional |
| priority | CharField | low / medium / high |
| status | CharField | pending / in_progress / completed / skipped |
| category | FK → Category | Nullable |
| reminder_sent | BooleanField | Backend-ready for reminders |

### `Category`
| Field | Type |
|-------|------|
| name | CharField |
| color | CharField (hex) |
| icon | CharField (emoji) |

### `DailyLog`
Auto-created/updated when tasks change. Tracks daily stats for the streak system.

---

## 🔌 URL Map

| URL | View | Name |
|-----|------|------|
| `/` | DashboardView | `dashboard` |
| `/task/new/` | TaskCreateView | `task_create` |
| `/task/<pk>/edit/` | TaskUpdateView | `task_edit` |
| `/task/<pk>/delete/` | TaskDeleteView | `task_delete` |
| `/task/<pk>/toggle/` | toggle_task_status (AJAX) | `task_toggle` |
| `/task/quick-add/` | quick_add_task | `task_quick_add` |
| `/history/` | HistoryView | `history` |
| `/admin/` | Django Admin | — |

---

## ⚙️ Configuration

### Change timezone (settings.py)
```python
TIME_ZONE = "Asia/Kolkata"   # or your local timezone
USE_TZ = True
```

### Switch to PostgreSQL (production)
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "dayflow",
        "USER": "postgres",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

### Create admin user
```bash
python manage.py createsuperuser
# Visit http://127.0.0.1:8000/admin
```

---

## 🔮 Extending (Ideas)

- **User auth** — add `user = FK(User)` to Task/DailyLog for multi-user support
- **Reminders** — `reminder_sent` field is ready; add Celery + django-celery-beat
- **Recurring tasks** — add `recurrence` field + management command
- **Drag-and-drop reorder** — use SortableJS on the task list
- **Calendar month view** — add a `/calendar/` view using existing DailyLog data
- **Export to CSV** — add a simple view that streams Task queryset as CSV
=======
# dayflow
>>>>>>> 73df2df9685056c73eed9806bde1e8613170e255
