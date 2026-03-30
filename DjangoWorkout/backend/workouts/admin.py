from django.contrib import admin

from .models import Exercise, MuscleGroup


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ("key", "label", "label_ru", "label_zh", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("key", "label", "label_ru", "label_zh")
    ordering = ("sort_order", "label")


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "muscle_group", "difficulty", "duration_seconds", "default_rest_seconds", "is_active")
    list_filter = ("muscle_group", "difficulty", "is_active")
    search_fields = ("name", "name_ru", "name_zh")
    ordering = ("muscle_group__sort_order", "difficulty", "name")
