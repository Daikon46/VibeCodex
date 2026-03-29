from rest_framework import serializers

from .models import Exercise


class WorkoutRequestSerializer(serializers.Serializer):
    muscle_groups = serializers.ListField(
        child=serializers.ChoiceField(choices=Exercise.MuscleGroup.values),
        allow_empty=False,
    )
    target_duration_minutes = serializers.IntegerField(min_value=5, max_value=180)

    def validate_muscle_groups(self, value):
        deduped = list(dict.fromkeys(value))
        if not deduped:
            raise serializers.ValidationError("Select at least one muscle group.")
        return deduped


class WorkoutItemSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    exercise_name = serializers.CharField()
    muscle_group = serializers.ChoiceField(choices=Exercise.MuscleGroup.values)
    difficulty = serializers.ChoiceField(choices=Exercise.Difficulty.values)
    duration_seconds = serializers.IntegerField()
    rest_seconds = serializers.IntegerField()


class WorkoutResponseSerializer(serializers.Serializer):
    feasible = serializers.BooleanField()
    target_duration_minutes = serializers.IntegerField()
    total_duration_minutes = serializers.FloatField()
    minimum_duration_minutes = serializers.FloatField(allow_null=True)
    muscle_groups = serializers.ListField(child=serializers.ChoiceField(choices=Exercise.MuscleGroup.values))
    items = WorkoutItemSerializer(many=True)
    message = serializers.CharField(allow_null=True)
