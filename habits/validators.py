from datetime import timedelta

from rest_framework.exceptions import ValidationError

from habits.models import Habit


def validate_exclusive_reward_related(data):
    """Проверка, чтобы исключить одновременный выбор связанной привычки и указания вознаграждения."""

    reward = data.get("award")
    related_habit = data.get("related_habit")
    if reward and related_habit:
        raise ValidationError(
            "Можно заполнить только одно из полей: 'reward' или 'related_habit'."
        )


def validate_related_habit_is_pleasant(data):
    """Проверка, что в связанные привычки попадают только привычки с признаком приятной привычки"""

    related_habit = data.get("related_habit")
    if related_habit:
        habit = Habit.objects.get(id=related_habit.id)
        if not habit.sign_of_pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной.")


def validate_pleasant_habit_no_reward_or_related(data):
    """Проверка, что у приятной привычки не может быть вознаграждения или связанной привычки."""
    from habits.models import Habit

    habits = Habit.objects.filter(sign_of_pleasant_habit=True)
    for habit in habits:
        if habit.award or habit.related_habit:
            raise ValidationError(
                f"Привычка '{habit}' не должна иметь вознаграждение или связанную привычку."
            )


def validate_time_to_complete(value):
    """Проверка, что время выполнения не превышает 120 секунд"""
    max_duration = timedelta(seconds=120)
    if value is None:
        value = timedelta(seconds=60)
    if value > max_duration:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_periodicity(value):
    """Проверка, что периодичность не превышает 7 дней."""

    if value is None:
        value = 1
    if not (0 < value <= 7):
        raise ValidationError("Периодичность должна быть в диапазоне от 1 до 7.")
