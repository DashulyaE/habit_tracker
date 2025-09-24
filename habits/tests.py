from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование CRUD операций для модели Привычка"""

    def setUp(self):
        self.user = User.objects.create(email="admin@test.ru")
        self.habit = Habit.objects.create(
            user=self.user,
            location="Дом",
            time="2025-09-22T16:25:00+03:00",
            action="Выпить витамин",
            sign_of_pleasant_habit=False,
            periodicity=1,
            time_to_complete="00:01:00",
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrive(self):
        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habits_create")
        data = {
            "location": "Дом",
            "time": "2025-09-22T13:25:00Z",
            "action": "Вода",
            "sign_of_pleasant_habit": False,
            "periodicity": 1,
            "award": "Чашка кофе",
            "time_to_complete": "00:01:00",
            "is_public": True,
            "user": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse("habits:habits_update", args=(self.habit.pk,))
        data = {"action": "Выпить витамин Д"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Выпить витамин Д")

    def test_habit_delete(self):
        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        url = reverse("habits:habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "location": self.habit.location,
                    "time": self.habit.time,
                    "action": self.habit.action,
                    "sign_of_pleasant_habit": False,
                    "periodicity": self.habit.periodicity,
                    "award": self.habit.award,
                    "time_to_complete": self.habit.time_to_complete,
                    "is_public": True,
                    "user": self.user.pk,
                    "related_habit": None,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
