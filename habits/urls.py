from django.contrib import admin
from django.urls import path, include
from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, HabitDestroyAPIView, \
    HabitUpdateAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path("habits/", HabitListAPIView.as_view(), name="habits_list"),
    path("habits/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habits_retrieve"),
    path("habits/create/", HabitCreateAPIView.as_view(), name="habits_create"),
    path("habits/<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habits_delete"),
    path("habits/<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habits_update"),
]
