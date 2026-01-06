from django.db import models
import random

# Create your models here.

class Session(models.Model):
    """Track a learning session for adaptive difficulty"""
    created_at = models.DateTimeField(auto_now_add=True)
    current_level = models.IntegerField(default=1)
    consecutive_correct = models.IntegerField(default=0)
    consecutive_incorrect = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Session {self.id} - Level {self.current_level}"


class ExerciseAttempt(models.Model):
    """Track individual exercise attempts"""
    EXERCISE_TYPES = [
        ('math', 'Math'),
        ('typing', 'Typing'),
        ('spelling', 'Spelling'),
    ]
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attempts')
    exercise_type = models.CharField(max_length=10, choices=EXERCISE_TYPES)
    question = models.TextField()
    correct_answer = models.TextField()
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    difficulty_level = models.IntegerField()
    time_taken = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.exercise_type} - Level {self.difficulty_level} - {'✓' if self.is_correct else '✗'}"

