from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MuscleGroup
from .serializers import WorkoutRequestSerializer, WorkoutResponseSerializer
from .services import WorkoutGenerationError, generate_workout


class MuscleGroupListView(APIView):
    def get(self, request):
        groups = [
            {
                "key": group.key,
                "label": group.label,
                "label_ru": group.label_ru,
                "label_zh": group.label_zh,
            }
            for group in MuscleGroup.objects.filter(is_active=True)
        ]
        return Response(groups)


class WorkoutGenerateView(APIView):
    def post(self, request):
        serializer = WorkoutRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            workout = generate_workout(**serializer.validated_data)
        except WorkoutGenerationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = WorkoutResponseSerializer(workout)
        return Response(response_serializer.data)

# Create your views here.
