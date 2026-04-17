from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    try:
        return round((float(value) / float(total)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def time_to_minutes(t):
    """Convert a time object to total minutes since midnight."""
    if t is None:
        return 0
    return t.hour * 60 + t.minute


@register.filter
def priority_emoji(priority):
    return {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(priority, "⚪")


@register.filter
def status_emoji(status):
    return {
        "completed": "✅",
        "in_progress": "⚡",
        "pending": "⏳",
        "skipped": "⏭",
    }.get(status, "⏳")
