from django.db import migrations


EXERCISES = [
    {"name": "Incline Push-Up", "muscle_group": "chest", "difficulty": "easy", "duration_seconds": 180, "default_rest_seconds": 40},
    {"name": "Chest Press", "muscle_group": "chest", "difficulty": "medium", "duration_seconds": 240, "default_rest_seconds": 45},
    {"name": "Bench Press", "muscle_group": "chest", "difficulty": "hard", "duration_seconds": 300, "default_rest_seconds": 60},
    {"name": "Resistance Band Row", "muscle_group": "back", "difficulty": "easy", "duration_seconds": 180, "default_rest_seconds": 40},
    {"name": "Lat Pulldown", "muscle_group": "back", "difficulty": "medium", "duration_seconds": 240, "default_rest_seconds": 45},
    {"name": "Deadlift", "muscle_group": "back", "difficulty": "hard", "duration_seconds": 300, "default_rest_seconds": 75},
    {"name": "Arm Circles", "muscle_group": "shoulders", "difficulty": "easy", "duration_seconds": 150, "default_rest_seconds": 30},
    {"name": "Dumbbell Shoulder Press", "muscle_group": "shoulders", "difficulty": "medium", "duration_seconds": 240, "default_rest_seconds": 45},
    {"name": "Push Press", "muscle_group": "shoulders", "difficulty": "hard", "duration_seconds": 300, "default_rest_seconds": 60},
    {"name": "Wrist Curl", "muscle_group": "hands", "difficulty": "easy", "duration_seconds": 150, "default_rest_seconds": 30},
    {"name": "Hammer Curl", "muscle_group": "hands", "difficulty": "medium", "duration_seconds": 210, "default_rest_seconds": 40},
    {"name": "Farmer Carry", "muscle_group": "hands", "difficulty": "hard", "duration_seconds": 240, "default_rest_seconds": 60},
    {"name": "Bodyweight Squat", "muscle_group": "legs", "difficulty": "easy", "duration_seconds": 180, "default_rest_seconds": 40},
    {"name": "Walking Lunge", "muscle_group": "legs", "difficulty": "medium", "duration_seconds": 240, "default_rest_seconds": 45},
    {"name": "Barbell Squat", "muscle_group": "legs", "difficulty": "hard", "duration_seconds": 300, "default_rest_seconds": 75},
]


def seed_exercises(apps, schema_editor):
    Exercise = apps.get_model("workouts", "Exercise")
    for exercise in EXERCISES:
        Exercise.objects.update_or_create(
            name=exercise["name"],
            defaults=exercise,
        )


def unseed_exercises(apps, schema_editor):
    Exercise = apps.get_model("workouts", "Exercise")
    Exercise.objects.filter(name__in=[exercise["name"] for exercise in EXERCISES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("workouts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_exercises, unseed_exercises),
    ]
