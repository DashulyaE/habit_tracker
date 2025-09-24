from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Создатель привычки",
    )
    location = models.CharField(
        max_length=250,
        default="Дом",
        verbose_name="Место",
        help_text="Место, в котором необходимо выполнять привычку",
    )
    time = models.DateTimeField(
        verbose_name="Время",
        help_text="Время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=250,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка",
    )
    sign_of_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Привычка, которую можно привязать к выполнению полезной привычки",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, которая указывается в качестве связанной для полезной привычки",
        blank=True,
        null=True,
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Периодичность выполнения привычки для напоминания в днях",
    )
    award = models.CharField(
        max_length=200,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения",
        blank=True,
        null=True,
    )
    time_to_complete = models.DurationField(
        verbose_name="Время на выполнение",
        help_text="Время, которое пользователь потратит на выполнение привычки",
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Признак публичности",
        help_text="Привычка в общем доступе,",
    )

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
