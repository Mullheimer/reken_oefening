from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Session, ExerciseAttempt
from .serializers import SessionSerializer, ExerciseAttemptSerializer
import random

def home(request):
    """Render the home page with navigation buttons"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reken Oefening - Home</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                    sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                text-align: center;
                background: white;
                border-radius: 20px;
                padding: 60px 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
            }
            
            h1 {
                color: #333;
                margin-bottom: 15px;
                font-size: 48px;
            }
            
            .subtitle {
                color: #666;
                margin-bottom: 50px;
                font-size: 18px;
            }
            
            .buttons {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .btn {
                padding: 15px 30px;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            
            .btn-secondary {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            
            .btn-secondary:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4);
            }
            
            .btn-tertiary {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
            }
            
            .btn-tertiary:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(79, 172, 254, 0.4);
            }
            
            .btn-admin {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                color: white;
            }
            
            .btn-admin:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(250, 112, 154, 0.4);
            }
            
            .footer {
                margin-top: 40px;
                color: #999;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Reken Oefening</h1>
            <p class="subtitle">Learn Math, Typing & Spelling with Adaptive Difficulty</p>
            
            <div class="buttons">
                <a href="/exercises/" class="btn btn-primary">📚 Start Learning</a>
                <a href="/api/" class="btn btn-secondary">🔌 API Documentation</a>
                <a href="/admin/" class="btn btn-admin">⚙️ Admin Panel</a>
            </div>
            
            <div class="footer">
                <p>Welcome to Reken Oefening - Your personal learning assistant</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def exercises_list(request):
    """Render the exercises selection page"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Choose Exercise - Reken Oefening</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                    sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            
            .navbar {
                max-width: 900px;
                margin: 0 auto 40px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
            
            .navbar h2 {
                color: #333;
                margin: 0;
            }
            
            .navbar a {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
                transition: color 0.3s ease;
            }
            
            .navbar a:hover {
                color: #764ba2;
            }
            
            .container {
                max-width: 900px;
                margin: 0 auto;
            }
            
            h1 {
                color: white;
                text-align: center;
                margin-bottom: 40px;
                font-size: 42px;
            }
            
            .exercises-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px;
            }
            
            .exercise-card {
                background: white;
                border-radius: 15px;
                padding: 40px 30px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                cursor: pointer;
                text-decoration: none;
                color: inherit;
            }
            
            .exercise-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }
            
            .exercise-icon {
                font-size: 60px;
                margin-bottom: 15px;
            }
            
            .exercise-card h3 {
                color: #333;
                margin-bottom: 10px;
                font-size: 24px;
            }
            
            .exercise-card p {
                color: #666;
                font-size: 14px;
                line-height: 1.6;
            }
            
            .exercise-card.math {
                border-top: 4px solid #667eea;
            }
            
            .exercise-card.typing {
                border-top: 4px solid #f093fb;
            }
            
            .exercise-card.spelling {
                border-top: 4px solid #4facfe;
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>🎓 Reken Oefening</h2>
            <a href="/">← Back to Home</a>
        </div>
        
        <div class="container">
            <h1>Choose an Exercise</h1>
            
            <div class="exercises-grid">
                <a href="/exercises/math/" class="exercise-card math">
                    <div class="exercise-icon">🧮</div>
                    <h3>Math Exercises</h3>
                    <p>Practice addition, subtraction, and multiplication with adaptive difficulty levels.</p>
                </a>
                
                <a href="/exercises/typing/" class="exercise-card typing">
                    <div class="exercise-icon">⌨️</div>
                    <h3>Typing Exercises</h3>
                    <p>Improve your typing speed and accuracy with engaging word exercises.</p>
                </a>
                
                <a href="/exercises/spelling/" class="exercise-card spelling">
                    <div class="exercise-icon">✏️</div>
                    <h3>Spelling Exercises</h3>
                    <p>Master spelling with progressive difficulty and instant feedback.</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def math_exercise(request):
    """Render the math exercise page"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Math Exercise - Reken Oefening</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .navbar {
                max-width: 800px;
                margin: 0 auto 30px;
                padding: 20px;
                background: white;
                border-radius: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            }
            .navbar h2 { margin: 0; color: #333; }
            .navbar a { 
                color: #667eea; 
                text-decoration: none; 
                font-weight: 600;
                padding: 10px 20px;
                border-radius: 8px;
                transition: background 0.3s;
            }
            .navbar a:hover { background: #f0f0f0; }
            
            .stats {
                max-width: 800px;
                margin: 0 auto 20px;
                padding: 15px;
                background: rgba(255,255,255,0.95);
                border-radius: 10px;
                display: flex;
                justify-content: space-around;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            }
            .stat-item {
                text-align: center;
            }
            .stat-value {
                font-size: 28px;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 60px 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            
            #loading {
                font-size: 24px;
                color: #667eea;
            }
            
            #question-container {
                display: none;
            }
            
            .question {
                font-size: 72px;
                font-weight: bold;
                color: #333;
                margin: 40px 0;
                min-height: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .answer-input {
                font-size: 48px;
                padding: 20px;
                border: 3px solid #ddd;
                border-radius: 15px;
                text-align: center;
                width: 300px;
                max-width: 100%;
                transition: border-color 0.3s;
            }
            .answer-input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .btn {
                display: inline-block;
                margin-top: 30px;
                padding: 18px 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 20px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.3s ease, box-shadow 0.3s;
            }
            .btn:hover { 
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            #feedback {
                margin-top: 30px;
                font-size: 24px;
                font-weight: bold;
                min-height: 40px;
            }
            .correct {
                color: #10b981;
            }
            .incorrect {
                color: #ef4444;
            }
            
            .level-badge {
                display: inline-block;
                padding: 10px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 20px;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 20px;
            }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background: #e5e7eb;
                border-radius: 10px;
                margin: 20px 0;
                overflow: hidden;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transition: width 0.5s ease;
                width: 0%;
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>🧮 Math Exercise</h2>
            <a href="/exercises/">← Back to Exercises</a>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-item">
                <div class="stat-value" id="level">1</div>
                <div class="stat-label">Level</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="correct">0</div>
                <div class="stat-label">Correct</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="streak">0</div>
                <div class="stat-label">Streak</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="total">0</div>
                <div class="stat-label">Total</div>
            </div>
        </div>
        
        <div class="container">
            <div id="loading">
                <p>🎯 Setting up your session...</p>
            </div>
            
            <div id="question-container">
                <div class="question" id="question">?</div>
                
                <input 
                    type="number" 
                    id="answer" 
                    class="answer-input" 
                    placeholder="?"
                    autofocus
                >
                
                <div>
                    <button class="btn" id="submit-btn" onclick="submitAnswer()">Check Answer</button>
                    <button class="btn" id="next-btn" onclick="nextQuestion()" style="display:none;">Next Question →</button>
                </div>
                
                <div id="feedback"></div>
                
                <div class="progress-bar">
                    <div class="progress-fill" id="progress"></div>
                </div>
            </div>
        </div>
        
        <script>
            let sessionId = null;
            let currentQuestion = null;
            let correctAnswer = null;
            let stats = {
                level: 1,
                correct: 0,
                streak: 0,
                total: 0
            };
            
            // Initialize session
            async function initSession() {
                try {
                    const response = await fetch('/api/sessions/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({})
                    });
                    const data = await response.json();
                    sessionId = data.id;
                    stats.level = data.current_level;
                    updateStats();
                    await loadQuestion();
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('question-container').style.display = 'block';
                } catch (error) {
                    console.error('Error creating session:', error);
                    document.getElementById('loading').innerHTML = '<p style="color: #ef4444;">Error starting session. Please refresh the page.</p>';
                }
            }
            
            // Load new question
            async function loadQuestion() {
                try {
                    const response = await fetch(`/api/exercises/generate_math/?session_id=${sessionId}`);
                    const data = await response.json();
                    currentQuestion = data.question;
                    correctAnswer = data.correct_answer;
                    stats.level = data.difficulty_level;
                    
                    document.getElementById('question').textContent = data.question;
                    document.getElementById('answer').value = '';
                    document.getElementById('answer').disabled = false;
                    document.getElementById('answer').focus();
                    document.getElementById('feedback').textContent = '';
                    document.getElementById('submit-btn').style.display = 'inline-block';
                    document.getElementById('next-btn').style.display = 'none';
                    updateStats();
                } catch (error) {
                    console.error('Error loading question:', error);
                }
            }
            
            // Submit answer
            async function submitAnswer() {
                const userAnswer = document.getElementById('answer').value;
                if (!userAnswer) {
                    alert('Please enter an answer!');
                    return;
                }
                
                const isCorrect = userAnswer === correctAnswer;
                stats.total++;
                
                // Save attempt
                try {
                    await fetch('/api/exercises/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session: sessionId,
                            exercise_type: 'math',
                            question: currentQuestion,
                            correct_answer: correctAnswer,
                            user_answer: userAnswer,
                            is_correct: isCorrect,
                            difficulty_level: stats.level
                        })
                    });
                    
                    // Update difficulty
                    await fetch(`/api/sessions/${sessionId}/update_difficulty/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            is_correct: isCorrect
                        })
                    });
                    
                    // Update session data
                    const sessionResponse = await fetch(`/api/sessions/${sessionId}/`);
                    const sessionData = await sessionResponse.json();
                    stats.level = sessionData.current_level;
                    stats.streak = sessionData.consecutive_correct;
                    
                } catch (error) {
                    console.error('Error saving attempt:', error);
                }
                
                // Show feedback
                const feedback = document.getElementById('feedback');
                if (isCorrect) {
                    stats.correct++;
                    feedback.textContent = '✓ Correct! Great job!';
                    feedback.className = 'correct';
                } else {
                    stats.streak = 0;
                    feedback.textContent = `✗ Incorrect. The answer was ${correctAnswer}`;
                    feedback.className = 'incorrect';
                }
                
                document.getElementById('answer').disabled = true;
                document.getElementById('submit-btn').style.display = 'none';
                document.getElementById('next-btn').style.display = 'inline-block';
                updateStats();
            }
            
            // Next question
            function nextQuestion() {
                loadQuestion();
            }
            
            // Update stats display
            function updateStats() {
                document.getElementById('level').textContent = stats.level;
                document.getElementById('correct').textContent = stats.correct;
                document.getElementById('streak').textContent = stats.streak;
                document.getElementById('total').textContent = stats.total;
                
                const progressPercent = stats.total > 0 ? (stats.correct / stats.total) * 100 : 0;
                document.getElementById('progress').style.width = progressPercent + '%';
            }
            
            // Handle Enter key
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('answer').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && !this.disabled) {
                        submitAnswer();
                    }
                });
                
                initSession();
            });
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

def typing_exercise(request):
    """Render the typing exercise page"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Typing Exercise - Reken Oefening</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .navbar {
                max-width: 700px;
                margin: 0 auto 30px;
                padding: 15px;
                background: white;
                border-radius: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .navbar h2 { margin: 0; color: #333; }
            .navbar a { color: #f5576c; text-decoration: none; font-weight: 600; }
            .container {
                max-width: 700px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 50px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            h1 { color: #333; margin-bottom: 40px; }
            .message { font-size: 18px; color: #666; line-height: 1.8; }
            .btn {
                display: inline-block;
                margin-top: 30px;
                padding: 15px 40px;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                transition: transform 0.3s ease;
            }
            .btn:hover { transform: translateY(-3px); }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>⌨️ Typing Exercise</h2>
            <a href="/exercises/">← Back</a>
        </div>
        <div class="container">
            <h1>Typing Exercise Coming Soon!</h1>
            <div class="message">
                <p>This interactive typing exercise will include:</p>
                <ul style="text-align: left; max-width: 400px; margin: 20px auto;">
                    <li>Dutch word typing practice</li>
                    <li>Progressive difficulty levels</li>
                    <li>Speed and accuracy tracking</li>
                    <li>Instant feedback</li>
                </ul>
                <p style="margin-top: 30px;">Use the API endpoints to integrate this feature!</p>
            </div>
            <a href="/api/" class="btn">View API Documentation</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def spelling_exercise(request):
    """Render the spelling exercise page"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Spelling Exercise - Reken Oefening</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .navbar {
                max-width: 700px;
                margin: 0 auto 30px;
                padding: 15px;
                background: white;
                border-radius: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .navbar h2 { margin: 0; color: #333; }
            .navbar a { color: #4facfe; text-decoration: none; font-weight: 600; }
            .container {
                max-width: 700px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 50px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
            }
            h1 { color: #333; margin-bottom: 40px; }
            .message { font-size: 18px; color: #666; line-height: 1.8; }
            .btn {
                display: inline-block;
                margin-top: 30px;
                padding: 15px 40px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                transition: transform 0.3s ease;
            }
            .btn:hover { transform: translateY(-3px); }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h2>✏️ Spelling Exercise</h2>
            <a href="/exercises/">← Back</a>
        </div>
        <div class="container">
            <h1>Spelling Exercise Coming Soon!</h1>
            <div class="message">
                <p>This interactive spelling exercise will include:</p>
                <ul style="text-align: left; max-width: 400px; margin: 20px auto;">
                    <li>Dutch word spelling challenges</li>
                    <li>Audio pronunciation hints</li>
                    <li>Adaptive difficulty levels</li>
                    <li>Progress tracking</li>
                </ul>
                <p style="margin-top: 30px;">Use the API endpoints to integrate this feature!</p>
            </div>
            <a href="/api/" class="btn">View API Documentation</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

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

