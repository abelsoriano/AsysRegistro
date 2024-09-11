from celery import shared_task
from .models import Miembro, Notification
from datetime import date

@shared_task
def check_birthdays():
    today = date.today()
    members = Miembro.objects.all()
    for member in members:
        if member.is_birthday_today():
            Notification.objects.create(
                message=f'¡Hoy es el cumpleaños de {member.name} {member.lastname}!'
            )
