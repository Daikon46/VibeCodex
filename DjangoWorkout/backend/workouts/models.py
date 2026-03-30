from django.core.validators import MinValueValidator
from django.db import models


class MuscleGroup(models.Model):
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    ARMS = "arms"
    LEGS = "legs"

    key = models.CharField(max_length=24, unique=True)
    label = models.CharField(max_length=64)
    label_ru = models.CharField(max_length=64)
    label_zh = models.CharField(max_length=64)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "label"]

    def __str__(self):
        return self.label


class Exercise(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    name = models.CharField(max_length=120, unique=True)
    name_ru = models.CharField(max_length=120, blank=True)
    name_zh = models.CharField(max_length=120, blank=True)
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.PROTECT,
        related_name="exercises",
    )
    difficulty = models.CharField(max_length=12, choices=Difficulty.choices)
    duration_seconds = models.PositiveIntegerField(validators=[MinValueValidator(30)])
    default_rest_seconds = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["muscle_group__sort_order", "difficulty", "duration_seconds", "name"]

    def __str__(self):
        return f"{self.name} ({self.muscle_group.label})"
