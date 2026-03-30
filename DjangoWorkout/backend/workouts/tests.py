from django.test import TestCase
from rest_framework.test import APIClient

from .models import Exercise, MuscleGroup
from .services import generate_workout


def create_muscle_group(key, label, label_ru, label_zh, sort_order):
    muscle_group, _ = MuscleGroup.objects.update_or_create(
        key=key,
        defaults={
            "label": label,
            "label_ru": label_ru,
            "label_zh": label_zh,
            "sort_order": sort_order,
            "is_active": True,
        },
    )
    return muscle_group


class WorkoutGenerationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        chest = create_muscle_group("chest", "Chest", "Грудь", "胸部", 1)
        back = create_muscle_group("back", "Back", "Спина", "背部", 2)
        Exercise.objects.filter(muscle_group__key__in=["chest", "back"]).delete()

        Exercise.objects.bulk_create(
            [
                Exercise(
                    name="Test Push-Up",
                    name_ru="Тестовое отжимание",
                    name_zh="测试俯卧撑",
                    muscle_group=chest,
                    difficulty=Exercise.Difficulty.EASY,
                    duration_seconds=180,
                    default_rest_seconds=45,
                ),
                Exercise(
                    name="Test Bench Press",
                    name_ru="Тестовый жим лежа",
                    name_zh="测试卧推",
                    muscle_group=chest,
                    difficulty=Exercise.Difficulty.HARD,
                    duration_seconds=240,
                    default_rest_seconds=60,
                ),
                Exercise(
                    name="Test Incline Press",
                    name_ru="Тестовый жим под углом",
                    name_zh="测试上斜推举",
                    muscle_group=chest,
                    difficulty=Exercise.Difficulty.MEDIUM,
                    duration_seconds=210,
                    default_rest_seconds=45,
                ),
                Exercise(
                    name="Test Lat Pulldown",
                    name_ru="Тестовая тяга верхнего блока",
                    name_zh="测试高位下拉",
                    muscle_group=back,
                    difficulty=Exercise.Difficulty.MEDIUM,
                    duration_seconds=240,
                    default_rest_seconds=45,
                ),
            ]
        )

    def test_generate_valid_workout(self):
        workout = generate_workout(["chest"], 15)

        self.assertTrue(workout["feasible"])
        self.assertEqual(workout["items"][0].exercise_name_ru, "Тестовое отжимание")
        self.assertEqual(workout["items"][0].exercise_name_zh, "测试俯卧撑")
        self.assertEqual(workout["items"][0].difficulty, Exercise.Difficulty.EASY)
        self.assertEqual(workout["items"][1].difficulty, Exercise.Difficulty.HARD)
        self.assertGreaterEqual(len(workout["items"]), 2)

    def test_returns_minimum_duration_when_target_too_short(self):
        workout = generate_workout(["chest"], 5)

        self.assertFalse(workout["feasible"])
        self.assertEqual(workout["minimum_duration_minutes"], 8)
        self.assertEqual(len(workout["items"]), 2)

    def test_supports_multiple_muscle_groups(self):
        workout = generate_workout(["chest", "back"], 20)

        self.assertTrue(workout["feasible"])
        self.assertIn(
            "back",
            {item.muscle_group for item in workout["items"]},
        )


class WorkoutApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        legs = create_muscle_group("legs", "Legs", "Ноги", "腿部", 5)
        Exercise.objects.filter(muscle_group__key="legs").delete()

        Exercise.objects.bulk_create(
            [
                Exercise(
                    name="Test Air Squat",
                    name_ru="Тестовый присед с весом тела",
                    name_zh="测试徒手深蹲",
                    muscle_group=legs,
                    difficulty=Exercise.Difficulty.EASY,
                    duration_seconds=180,
                    default_rest_seconds=45,
                ),
                Exercise(
                    name="Test Barbell Squat",
                    name_ru="Тестовый присед со штангой",
                    name_zh="测试杠铃深蹲",
                    muscle_group=legs,
                    difficulty=Exercise.Difficulty.HARD,
                    duration_seconds=240,
                    default_rest_seconds=60,
                ),
            ]
        )

    def setUp(self):
        self.client = APIClient()

    def test_lists_muscle_groups(self):
        response = self.client.get("/api/muscle-groups/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item["key"] == "legs" for item in response.json()))
        self.assertTrue(any(item["label_ru"] == "Ноги" for item in response.json()))

    def test_validates_unknown_muscle_group(self):
        response = self.client.post(
            "/api/workouts/generate/",
            {"muscle_groups": ["core"], "target_duration_minutes": 20},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_generates_workout(self):
        response = self.client.post(
            "/api/workouts/generate/",
            {"muscle_groups": ["legs"], "target_duration_minutes": 12},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.json())
        self.assertEqual(response.json()["items"][0]["exercise_name_ru"], "Тестовый присед с весом тела")
        self.assertEqual(response.json()["items"][0]["exercise_name_zh"], "测试徒手深蹲")
