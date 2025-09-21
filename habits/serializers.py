from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    """Сериализатор модели Привычка"""

    class Meta:
        model = Habit
        fields = "__all__"