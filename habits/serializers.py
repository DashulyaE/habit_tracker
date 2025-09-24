from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import (
    validate_exclusive_reward_related,
    validate_related_habit_is_pleasant,
    validate_pleasant_habit_no_reward_or_related,
    validate_time_to_complete,
    validate_periodicity,
)


class HabitSerializer(ModelSerializer):
    """Сериализатор модели Привычка"""

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        validate_exclusive_reward_related(data)
        validate_related_habit_is_pleasant(data)
        validate_pleasant_habit_no_reward_or_related(data)
        validate_time_to_complete(data.get("time_to_complete"))
        validate_periodicity(data.get("periodicity"))

        if data.get("sign_of_pleasant_habit"):
            if data.get("award") or data.get("related_habit"):
                raise serializers.ValidationError(
                    "У приятной привычки не должно быть вознаграждения или связанной привычки."
                )
        return data
