from django.contrib import admin
from .models import Session, ExerciseAttempt

# Register your models here.

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'current_level', 'consecutive_correct', 'consecutive_incorrect']
    list_filter = ['current_level', 'created_at']
    readonly_fields = ['created_at']


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'exercise_type', 'is_correct', 'difficulty_level', 'created_at']
    list_filter = ['exercise_type', 'is_correct', 'difficulty_level', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['question', 'user_answer', 'correct_answer']
