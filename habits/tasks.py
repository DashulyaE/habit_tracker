from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Habit

from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # Получаем привычки, запланированные на сегодня
    habits_today = Habit.objects.filter(time__gte=today_start, time__lt=today_end)

    # Группируем привычки по пользователям
    user_habits = {}
    for habit in habits_today:
        user_id = habit.user.id if habit.user else None
        if user_id:
            user_habits.setdefault(user_id, []).append(habit)

    # Для каждого пользователя отправляем сообщение
    for user_id, habits in user_habits.items():
        user = habits[0].user
        chat_id = user.tg_chat_id
        if chat_id:
            habit_list = "\n".join(
                [f"{habit.action} в {habit.time.strftime('%H:%M')}" for habit in habits]
            )
            message = f"Сегодня у вас запланированы привычки:\n{habit_list}"
            send_telegram_message(chat_id, message)
