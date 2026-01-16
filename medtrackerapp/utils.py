from django.utils import timezone

def days_since(date):
    now = timezone.now()
    delta = now.date() - date
    return delta.days
