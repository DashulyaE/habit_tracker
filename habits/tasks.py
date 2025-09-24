from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Habit

from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    """Задача, которая получает привычки пользователя за текущий день и отправляет уведомление о них в телеграм"""

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    habits_today = Habit.objects.filter(time__gte=today_start, time__lt=today_end)

    user_habits = {}
    for habit in habits_today:
        user_id = habit.user.id if habit.user else None
        if user_id:
            user_habits.setdefault(user_id, []).append(habit)

    for user_id, habits in user_habits.items():
        user = habits[0].user
        chat_id = user.tg_chat_id
        if chat_id:
            habit_list = "\n".join(
                [f"{habit.action} в {habit.time.strftime('%H:%M')}" for habit in habits]
            )
            message = f"Сегодня у вас запланированы привычки:\n{habit_list}"
            send_telegram_message(chat_id, message)
