from dataclasses import dataclass
from math import ceil

from .models import Exercise


class WorkoutGenerationError(Exception):
    pass


@dataclass(frozen=True)
class PlannedItem:
    order: int
    exercise_name: str
    muscle_group: str
    difficulty: str
    duration_seconds: int
    rest_seconds: int


def _calculate_total_seconds(exercises):
    total = 0
    for index, exercise in enumerate(exercises):
        total += exercise.duration_seconds
        if index < len(exercises) - 1:
            total += exercise.default_rest_seconds
    return total


def _serialize_items(exercises):
    items = []
    for index, exercise in enumerate(exercises, start=1):
        rest_seconds = exercise.default_rest_seconds if index < len(exercises) else 0
        items.append(
            PlannedItem(
                order=index,
                exercise_name=exercise.name,
                muscle_group=exercise.muscle_group,
                difficulty=exercise.difficulty,
                duration_seconds=exercise.duration_seconds,
                rest_seconds=rest_seconds,
            )
        )
    return items


def _select_baseline(easy_exercises, hard_exercises):
    candidates = []
    for easy in easy_exercises:
        for hard in hard_exercises:
            if easy.pk == hard.pk:
                continue
            plan = [easy, hard]
            candidates.append((_calculate_total_seconds(plan), plan))
    if not candidates:
        raise WorkoutGenerationError(
            "Not enough exercise data to create a valid workout. Add at least one easy and one hard exercise."
        )
    _, best_plan = min(candidates, key=lambda candidate: candidate[0])
    return best_plan


def _append_mediums(plan, medium_exercises, target_seconds):
    used_ids = {exercise.pk for exercise in plan}
    remaining_pool = [exercise for exercise in medium_exercises if exercise.pk not in used_ids]
    reusable_pool = [exercise for exercise in medium_exercises if exercise.pk in used_ids]

    while True:
        current_total = _calculate_total_seconds(plan)
        if current_total >= target_seconds:
            return plan

        appended = False
        for exercise in [*remaining_pool, *reusable_pool]:
            added_seconds = plan[-1].default_rest_seconds + exercise.duration_seconds
            if current_total + added_seconds <= target_seconds:
                plan.append(exercise)
                remaining_pool = [item for item in remaining_pool if item.pk != exercise.pk]
                appended = True
                break

        if not appended:
            return plan


def generate_workout(muscle_groups, target_duration_minutes):
    exercises = list(
        Exercise.objects.filter(muscle_group__in=muscle_groups, is_active=True)
    )
    if not exercises:
        raise WorkoutGenerationError("No exercises are available for the selected muscle groups.")

    easy_exercises = [exercise for exercise in exercises if exercise.difficulty == Exercise.Difficulty.EASY]
    hard_exercises = [exercise for exercise in exercises if exercise.difficulty == Exercise.Difficulty.HARD]
    medium_exercises = sorted(
        [exercise for exercise in exercises if exercise.difficulty == Exercise.Difficulty.MEDIUM],
        key=lambda exercise: (exercise.duration_seconds, exercise.name),
    )

    baseline = _select_baseline(easy_exercises, hard_exercises)
    minimum_duration_seconds = _calculate_total_seconds(baseline)
    target_seconds = target_duration_minutes * 60

    if minimum_duration_seconds > target_seconds:
        return {
            "feasible": False,
            "target_duration_minutes": target_duration_minutes,
            "total_duration_minutes": round(minimum_duration_seconds / 60, 1),
            "minimum_duration_minutes": ceil(minimum_duration_seconds / 60),
            "muscle_groups": muscle_groups,
            "items": _serialize_items(baseline),
            "message": "The selected duration is too short. Use the minimum duration shown to keep the easy-then-hard pattern.",
        }

    completed_plan = _append_mediums(list(baseline), medium_exercises, target_seconds)
    total_duration_seconds = _calculate_total_seconds(completed_plan)
    return {
        "feasible": True,
        "target_duration_minutes": target_duration_minutes,
        "total_duration_minutes": round(total_duration_seconds / 60, 1),
        "minimum_duration_minutes": None,
        "muscle_groups": muscle_groups,
        "items": _serialize_items(completed_plan),
        "message": None,
    }
