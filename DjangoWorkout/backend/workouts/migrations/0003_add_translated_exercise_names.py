from django.db import migrations, models


EXERCISE_TRANSLATIONS = {
    "Incline Push-Up": {"name_ru": "Отжимания под наклоном", "name_zh": "上斜俯卧撑"},
    "Chest Press": {"name_ru": "Жим от груди", "name_zh": "卧推器推胸"},
    "Bench Press": {"name_ru": "Жим лежа", "name_zh": "卧推"},
    "Resistance Band Row": {"name_ru": "Тяга резиновой ленты", "name_zh": "弹力带划船"},
    "Lat Pulldown": {"name_ru": "Тяга верхнего блока", "name_zh": "高位下拉"},
    "Deadlift": {"name_ru": "Становая тяга", "name_zh": "硬拉"},
    "Arm Circles": {"name_ru": "Круги руками", "name_zh": "手臂绕环"},
    "Dumbbell Shoulder Press": {"name_ru": "Жим гантелей над головой", "name_zh": "哑铃肩推"},
    "Push Press": {"name_ru": "Толчковый жим", "name_zh": "借力推举"},
    "Wrist Curl": {"name_ru": "Сгибание кистей", "name_zh": "腕弯举"},
    "Hammer Curl": {"name_ru": "Молотковые сгибания", "name_zh": "锤式弯举"},
    "Farmer Carry": {"name_ru": "Фермерская прогулка", "name_zh": "农夫行走"},
    "Bodyweight Squat": {"name_ru": "Приседания с собственным весом", "name_zh": "徒手深蹲"},
    "Walking Lunge": {"name_ru": "Выпады в ходьбе", "name_zh": "行进弓步"},
    "Barbell Squat": {"name_ru": "Приседания со штангой", "name_zh": "杠铃深蹲"},
}


def populate_translated_names(apps, schema_editor):
    Exercise = apps.get_model("workouts", "Exercise")
    for exercise_name, translations in EXERCISE_TRANSLATIONS.items():
        Exercise.objects.filter(name=exercise_name).update(**translations)


def clear_translated_names(apps, schema_editor):
    Exercise = apps.get_model("workouts", "Exercise")
    Exercise.objects.update(name_ru="", name_zh="")


class Migration(migrations.Migration):
    dependencies = [
        ("workouts", "0002_seed_exercises"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercise",
            name="name_ru",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="exercise",
            name="name_zh",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.RunPython(populate_translated_names, clear_translated_names),
    ]
