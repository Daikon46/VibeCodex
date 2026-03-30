from django.db import migrations, models
import django.db.models.deletion


MUSCLE_GROUPS = [
    {"key": "chest", "label": "Chest", "label_ru": "Грудь", "label_zh": "胸部", "sort_order": 1},
    {"key": "back", "label": "Back", "label_ru": "Спина", "label_zh": "背部", "sort_order": 2},
    {"key": "shoulders", "label": "Shoulders", "label_ru": "Плечи", "label_zh": "肩部", "sort_order": 3},
    {"key": "arms", "label": "Arms", "label_ru": "Руки", "label_zh": "手臂", "sort_order": 4},
    {"key": "legs", "label": "Legs", "label_ru": "Ноги", "label_zh": "腿部", "sort_order": 5},
]

LEGACY_TO_KEY = {
    "chest": "chest",
    "back": "back",
    "shoulders": "shoulders",
    "hands": "arms",
    "arms": "arms",
    "legs": "legs",
}


def populate_muscle_groups(apps, schema_editor):
    Exercise = apps.get_model("workouts", "Exercise")
    MuscleGroup = apps.get_model("workouts", "MuscleGroup")

    group_map = {}
    for group in MUSCLE_GROUPS:
        obj, _ = MuscleGroup.objects.update_or_create(
            key=group["key"],
            defaults={
                "label": group["label"],
                "label_ru": group["label_ru"],
                "label_zh": group["label_zh"],
                "sort_order": group["sort_order"],
                "is_active": True,
            },
        )
        group_map[group["key"]] = obj

    for exercise in Exercise.objects.all():
        target_key = LEGACY_TO_KEY.get(exercise.muscle_group, exercise.muscle_group)
        exercise.muscle_group_ref = group_map[target_key]
        exercise.save(update_fields=["muscle_group_ref"])


def unpopulate_muscle_groups(apps, schema_editor):
    Exercise = apps.get_model("workouts", "Exercise")
    MuscleGroup = apps.get_model("workouts", "MuscleGroup")

    reverse_map = {
        "chest": "chest",
        "back": "back",
        "shoulders": "shoulders",
        "arms": "hands",
        "legs": "legs",
    }

    for exercise in Exercise.objects.select_related("muscle_group_ref"):
        if exercise.muscle_group_ref_id:
            exercise.muscle_group = reverse_map.get(exercise.muscle_group_ref.key, exercise.muscle_group_ref.key)
            exercise.save(update_fields=["muscle_group"])

    MuscleGroup.objects.filter(key__in=[group["key"] for group in MUSCLE_GROUPS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("workouts", "0003_add_translated_exercise_names"),
    ]

    operations = [
        migrations.CreateModel(
            name="MuscleGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=24, unique=True)),
                ("label", models.CharField(max_length=64)),
                ("label_ru", models.CharField(max_length=64)),
                ("label_zh", models.CharField(max_length=64)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["sort_order", "label"],
            },
        ),
        migrations.AddField(
            model_name="exercise",
            name="muscle_group_ref",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="workouts.musclegroup",
            ),
        ),
        migrations.RunPython(populate_muscle_groups, unpopulate_muscle_groups),
        migrations.RemoveField(
            model_name="exercise",
            name="muscle_group",
        ),
        migrations.RenameField(
            model_name="exercise",
            old_name="muscle_group_ref",
            new_name="muscle_group",
        ),
        migrations.AlterField(
            model_name="exercise",
            name="muscle_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="exercises",
                to="workouts.musclegroup",
            ),
        ),
        migrations.AlterModelOptions(
            name="exercise",
            options={"ordering": ["muscle_group__sort_order", "difficulty", "duration_seconds", "name"]},
        ),
    ]
