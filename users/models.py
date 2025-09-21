from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс Пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=50, verbose_name="Страна", blank=True, help_text="Укажите страну"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    tg_nick = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Tg name",
        help_text="Укажите ник в телеграм",
    )

    tg_chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Телеграм chat_id')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
