from django.core.validators import MinValueValidator
from django.db import models


class Exercise(models.Model):
    class MuscleGroup(models.TextChoices):
        CHEST = "chest", "Chest"
        BACK = "back", "Back"
        SHOULDERS = "shoulders", "Shoulders"
        HANDS = "hands", "Hands"
        LEGS = "legs", "Legs"

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    name = models.CharField(max_length=120, unique=True)
    name_ru = models.CharField(max_length=120, blank=True)
    name_zh = models.CharField(max_length=120, blank=True)
    muscle_group = models.CharField(max_length=24, choices=MuscleGroup.choices)
    difficulty = models.CharField(max_length=12, choices=Difficulty.choices)
    duration_seconds = models.PositiveIntegerField(validators=[MinValueValidator(30)])
    default_rest_seconds = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["muscle_group", "difficulty", "duration_seconds", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_muscle_group_display()})"

# Create your models here.
