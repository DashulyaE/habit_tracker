from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habit
from habits.paginations import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Создаем привычку и отправляем сообщение пользователю в Телеграм"""
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()


class HabitListAPIView(ListAPIView):
    """Прсомотр списка привычек"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    """Просмотр одной привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class HabitUpdateAPIView(UpdateAPIView):
    """Изменение привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class HabitPublicListAPIView(ListAPIView):
    """Просмотр опубликованных привычек"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [AllowAny]
    pagination_class = HabitPagination
