from rest_framework import serializers

from .models import Exercise, MuscleGroup


class WorkoutRequestSerializer(serializers.Serializer):
    muscle_groups = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
    target_duration_minutes = serializers.IntegerField(min_value=5, max_value=180)

    def validate_muscle_groups(self, value):
        deduped = list(dict.fromkeys(value))
        if not deduped:
            raise serializers.ValidationError("Select at least one muscle group.")
        available_keys = set(
            MuscleGroup.objects.filter(key__in=deduped, is_active=True).values_list("key", flat=True)
        )
        invalid_keys = [key for key in deduped if key not in available_keys]
        if invalid_keys:
            raise serializers.ValidationError("Select valid muscle groups.")
        return deduped


class WorkoutItemSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    exercise_name = serializers.CharField()
    exercise_name_ru = serializers.CharField()
    exercise_name_zh = serializers.CharField()
    muscle_group = serializers.CharField()
    difficulty = serializers.ChoiceField(choices=Exercise.Difficulty.values)
    duration_seconds = serializers.IntegerField()
    rest_seconds = serializers.IntegerField()


class WorkoutResponseSerializer(serializers.Serializer):
    feasible = serializers.BooleanField()
    target_duration_minutes = serializers.IntegerField()
    total_duration_minutes = serializers.FloatField()
    minimum_duration_minutes = serializers.FloatField(allow_null=True)
    muscle_groups = serializers.ListField(child=serializers.CharField())
    items = WorkoutItemSerializer(many=True)
    message = serializers.CharField(allow_null=True)
