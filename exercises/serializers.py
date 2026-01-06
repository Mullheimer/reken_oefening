from rest_framework import serializers
from .models import Session, ExerciseAttempt


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'created_at', 'current_level', 'consecutive_correct', 'consecutive_incorrect']


class ExerciseAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAttempt
        fields = ['id', 'session', 'exercise_type', 'question', 'correct_answer', 
                  'user_answer', 'is_correct', 'difficulty_level', 'time_taken', 'created_at']
        read_only_fields = ['created_at']
