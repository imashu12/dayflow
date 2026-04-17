#!/usr/bin/env python
"""
Setup script: runs migrations and seeds default categories + sample tasks.
Run once: python setup.py
"""
import os, sys, django, datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dayflow.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command
from planner.models import Category, Task

print("⚡ Running migrations...")
call_command("migrate", verbosity=0)

print("🌱 Seeding categories...")
CATEGORIES = [
    {"name": "Work",     "color": "#6366f1", "icon": "💼"},
    {"name": "Study",    "color": "#8b5cf6", "icon": "📚"},
    {"name": "Health",   "color": "#22c55e", "icon": "💪"},
    {"name": "Personal", "color": "#f59e0b", "icon": "🌟"},
    {"name": "Social",   "color": "#ec4899", "icon": "👥"},
    {"name": "Finance",  "color": "#14b8a6", "icon": "💰"},
]
cats = {}
for c in CATEGORIES:
    obj, _ = Category.objects.get_or_create(name=c["name"], defaults=c)
    cats[c["name"]] = obj
print(f"  ✓ {len(CATEGORIES)} categories ready")

print("📅 Seeding sample tasks for today...")
today = datetime.date.today()
TASKS = [
    {"title": "Morning workout", "start_time": "07:00", "end_time": "07:45", "priority": "high",   "category": "Health",   "description": "30 min run + stretching"},
    {"title": "Check emails",    "start_time": "09:00", "end_time": "09:30", "priority": "medium", "category": "Work",     "description": "Inbox zero routine"},
    {"title": "Deep work block", "start_time": "10:00", "end_time": "12:00", "priority": "high",   "category": "Work",     "description": "Focus session — no interruptions"},
    {"title": "Lunch break",     "start_time": "12:30", "end_time": "13:15", "priority": "low",    "category": "Personal", "description": ""},
    {"title": "Study session",   "start_time": "14:00", "end_time": "15:30", "priority": "high",   "category": "Study",    "description": "Review notes and practice problems"},
    {"title": "Team standup",    "start_time": "16:00", "end_time": "16:30", "priority": "medium", "category": "Work",     "description": "Daily sync with team"},
    {"title": "Evening walk",    "start_time": "18:30", "end_time": "19:00", "priority": "low",    "category": "Health",   "description": ""},
    {"title": "Read 30 pages",   "start_time": "21:00", "end_time": "21:30", "priority": "medium", "category": "Personal", "description": "Current book: Deep Work"},
]
for i, t in enumerate(TASKS):
    if not Task.objects.filter(title=t["title"], date=today).exists():
        Task.objects.create(
            title=t["title"],
            description=t.get("description",""),
            date=today,
            start_time=t["start_time"],
            end_time=t["end_time"],
            priority=t["priority"],
            category=cats[t["category"]],
            status="completed" if i < 2 else "pending",
        )
print(f"  ✓ Sample tasks created")

print("\n✅ Setup complete!")
print("   Run: python manage.py runserver")
print("   Open: http://127.0.0.1:8000")
