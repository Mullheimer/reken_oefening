from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Session, ExerciseAttempt
from .serializers import SessionSerializer, ExerciseAttemptSerializer
import random

# Create your views here.

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    
    @action(detail=True, methods=['post'])
    def update_difficulty(self, request, pk=None):
        """Update session difficulty based on answer correctness"""
        session = self.get_object()
        is_correct = request.data.get('is_correct', False)
        
        if is_correct:
            session.consecutive_correct += 1
            session.consecutive_incorrect = 0
            # Increase difficulty after 3 correct answers
            if session.consecutive_correct >= 3:
                session.current_level = min(session.current_level + 1, 10)
                session.consecutive_correct = 0
        else:
            session.consecutive_incorrect += 1
            session.consecutive_correct = 0
            # Decrease difficulty after 2 incorrect answers
            if session.consecutive_incorrect >= 2:
                session.current_level = max(session.current_level - 1, 1)
                session.consecutive_incorrect = 0
        
        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data)


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = ExerciseAttempt.objects.all()
    serializer_class = ExerciseAttemptSerializer
    
    @action(detail=False, methods=['get'])
    def generate_math(self, request):
        """Generate a math exercise based on difficulty level"""
        session_id = request.query_params.get('session_id')
        
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
        
        level = session.current_level
        
        # Generate math problems based on level (up to 200)
        if level <= 2:
            # Addition up to 20
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operation = '+'
            answer = num1 + num2
        elif level <= 4:
            # Addition up to 50
            num1 = random.randint(1, 25)
            num2 = random.randint(1, 25)
            operation = '+'
            answer = num1 + num2
        elif level <= 6:
            # Addition/Subtraction up to 100
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)
            operation = random.choice(['+', '-'])
            answer = num1 + num2 if operation == '+' else num1 - num2
            if answer < 0:
                num1, num2 = num2, num1
                answer = num1 - num2
        else:
            # Addition/Subtraction up to 200
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            operation = random.choice(['+', '-'])
            answer = num1 + num2 if operation == '+' else num1 - num2
            if answer < 0:
                num1, num2 = num2, num1
                answer = num1 - num2
        
        question = f"{num1} {operation} {num2}"
        
        return Response({
            'question': question,
            'correct_answer': str(answer),
            'difficulty_level': level,
            'exercise_type': 'math'
        })
    
    @action(detail=False, methods=['get'])
    def generate_typing(self, request):
        """Generate a typing exercise based on difficulty level"""
        session_id = request.query_params.get('session_id')
        
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
        
        level = session.current_level
        
        # Word lists for typing exercises (Dutch words for group 5)
        easy_words = ['kat', 'hond', 'boom', 'zon', 'maan', 'rood', 'blauw', 'huis']
        medium_words = ['fiets', 'school', 'vrienden', 'vakantie', 'speeltuin', 'computer']
        hard_words = ['bibliotheek', 'verjaardagsfeest', 'regenboog', 'avontuur', 'chocolade']
        
        if level <= 3:
            word = random.choice(easy_words)
        elif level <= 6:
            word = random.choice(medium_words)
        else:
            word = random.choice(hard_words)
        
        return Response({
            'question': word,
            'correct_answer': word,
            'difficulty_level': level,
            'exercise_type': 'typing'
        })
    
    @action(detail=False, methods=['get'])
    def generate_spelling(self, request):
        """Generate a spelling exercise based on difficulty level"""
        session_id = request.query_params.get('session_id')
        
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
        
        level = session.current_level
        
        # Spelling word lists (Dutch words with common spelling challenges)
        easy_words = [
            ('kat', 'k-a-t'),
            ('hond', 'h-o-n-d'),
            ('boom', 'b-o-o-m'),
            ('rood', 'r-o-o-d'),
        ]
        medium_words = [
            ('school', 's-ch-oo-l'),
            ('fiets', 'f-ie-ts'),
            ('vrienden', 'vr-ie-n-d-en'),
            ('straat', 's-tr-aa-t'),
        ]
        hard_words = [
            ('bibliotheek', 'b-i-b-l-i-o-th-eek'),
            ('verjaardagsfeest', 'v-er-j-aar-d-a-g-s-f-ee-s-t'),
            ('chocolade', 'ch-o-c-o-l-a-d-e'),
        ]
        
        if level <= 3:
            word, hint = random.choice(easy_words)
        elif level <= 6:
            word, hint = random.choice(medium_words)
        else:
            word, hint = random.choice(hard_words)
        
        return Response({
            'question': f'Spel het woord: {hint}',
            'correct_answer': word,
            'difficulty_level': level,
            'exercise_type': 'spelling'
        })

