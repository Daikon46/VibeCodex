from django.contrib import admin

from .models import Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "muscle_group", "difficulty", "duration_seconds", "default_rest_seconds", "is_active")
    list_filter = ("muscle_group", "difficulty", "is_active")
    search_fields = ("name",)
    ordering = ("muscle_group", "difficulty", "name")

# Register your models here.
