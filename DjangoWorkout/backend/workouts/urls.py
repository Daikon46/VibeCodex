from django.urls import path

from .views import MuscleGroupListView, WorkoutGenerateView

urlpatterns = [
    path("muscle-groups/", MuscleGroupListView.as_view(), name="muscle-group-list"),
    path("workouts/generate/", WorkoutGenerateView.as_view(), name="workout-generate"),
]
