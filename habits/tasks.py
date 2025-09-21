from celery import shared_task

from habits.services import send_telegram_message

@shared_task
def add():
    print("Hellow")