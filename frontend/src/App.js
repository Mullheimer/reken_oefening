import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [currentLevel, setCurrentLevel] = useState(1);
  const [exerciseType, setExerciseType] = useState('math');
  const [exercise, setExercise] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedback, setFeedback] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [score, setScore] = useState(0);
  const [totalAttempts, setTotalAttempts] = useState(0);
  const inputRef = useRef(null);

  // Create a new session on mount
  useEffect(() => {
    createSession();
  }, []);

  // Timer for time pressure
  useEffect(() => {
    if (startTime && !showFeedback) {
      const interval = setInterval(() => {
        setTimeElapsed(Math.floor((Date.now() - startTime) / 1000));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [startTime, showFeedback]);

  // Auto-focus input after exercise loads
  useEffect(() => {
    if (exercise && inputRef.current) {
      inputRef.current.focus();
    }
  }, [exercise]);

  const createSession = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/sessions/`, {
        current_level: 1,
        consecutive_correct: 0,
        consecutive_incorrect: 0
      });
      setSessionId(response.data.id);
      setCurrentLevel(response.data.current_level);
      generateExercise(response.data.id, 'math');
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const generateExercise = async (sid, type) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/exercises/generate_${type}/`, {
        params: { session_id: sid || sessionId }
      });
      setExercise(response.data);
      setUserAnswer('');
      setStartTime(Date.now());
      setTimeElapsed(0);
      setShowFeedback(false);
      setFeedback('');
    } catch (error) {
      console.error('Error generating exercise:', error);
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) return;

    const isCorrect = userAnswer.toLowerCase().trim() === exercise.correct_answer.toLowerCase().trim();
    const timeTaken = (Date.now() - startTime) / 1000;

    // Save attempt
    try {
      await axios.post(`${API_BASE_URL}/exercises/`, {
        session: sessionId,
        exercise_type: exerciseType,
        question: exercise.question,
        correct_answer: exercise.correct_answer,
        user_answer: userAnswer,
        is_correct: isCorrect,
        difficulty_level: currentLevel,
        time_taken: timeTaken
      });

      // Update difficulty
      const sessionResponse = await axios.post(
        `${API_BASE_URL}/sessions/${sessionId}/update_difficulty/`,
        { is_correct: isCorrect }
      );
      setCurrentLevel(sessionResponse.data.current_level);

      // Update score
      if (isCorrect) {
        setScore(score + 1);
      }
      setTotalAttempts(totalAttempts + 1);

      // Show positive feedback only
      if (isCorrect) {
        const positiveFeedback = [
          'Super gedaan! 🌟',
          'Geweldig! 👏',
          'Perfect! ✨',
          'Goed zo! 🎉',
          'Uitstekend! 💚'
        ];
        setFeedback(positiveFeedback[Math.floor(Math.random() * positiveFeedback.length)]);
      } else {
        setFeedback('Probeer het nog eens! 💪');
      }
      
      setShowFeedback(true);

      // Move to next exercise after brief delay
      setTimeout(() => {
        generateExercise(sessionId, exerciseType);
      }, 1500);
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const changeExerciseType = (type) => {
    setExerciseType(type);
    generateExercise(sessionId, type);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !showFeedback) {
      submitAnswer();
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Oefenplatform 🌱</h1>
        <div style={styles.stats}>
          <span style={styles.statItem}>Niveau: {currentLevel}</span>
          <span style={styles.statItem}>Score: {score}/{totalAttempts}</span>
        </div>
      </div>

      <div style={styles.exerciseTypeContainer}>
        <button
          style={{
            ...styles.typeButton,
            ...(exerciseType === 'math' ? styles.typeButtonActive : {})
          }}
          onClick={() => changeExerciseType('math')}
        >
          Rekenen
        </button>
        <button
          style={{
            ...styles.typeButton,
            ...(exerciseType === 'typing' ? styles.typeButtonActive : {})
          }}
          onClick={() => changeExerciseType('typing')}
        >
          Typen
        </button>
        <button
          style={{
            ...styles.typeButton,
            ...(exerciseType === 'spelling' ? styles.typeButtonActive : {})
          }}
          onClick={() => changeExerciseType('spelling')}
        >
          Spelling
        </button>
      </div>

      {exercise && (
        <div style={styles.exerciseCard}>
          <div style={styles.questionContainer}>
            <h2 style={styles.question}>{exercise.question}</h2>
            {!showFeedback && (
              <div style={styles.timerContainer}>
                <div style={{
                  ...styles.timerBar,
                  width: `${Math.min((timeElapsed / 30) * 100, 100)}%`
                }} />
              </div>
            )}
          </div>

          {!showFeedback ? (
            <div style={styles.answerContainer}>
              <input
                ref={inputRef}
                type="text"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type je antwoord..."
                style={styles.input}
              />
              <button onClick={submitAnswer} style={styles.submitButton}>
                Controleer ✓
              </button>
            </div>
          ) : (
            <div style={styles.feedbackContainer}>
              <p style={styles.feedback}>{feedback}</p>
            </div>
          )}
        </div>
      )}

      <div style={styles.encouragement}>
        <p style={styles.encouragementText}>
          {totalAttempts < 5 && "Ga zo door! Je doet het geweldig! 💚"}
          {totalAttempts >= 5 && totalAttempts < 10 && "Wat een mooie voortgang! 🌟"}
          {totalAttempts >= 10 && "Jij bent een ster! Blijf oefenen! ✨"}
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#e8f5e9',
    padding: '20px',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  title: {
    color: '#2e7d32',
    fontSize: '2.5rem',
    marginBottom: '10px',
  },
  stats: {
    display: 'flex',
    justifyContent: 'center',
    gap: '30px',
    marginTop: '10px',
  },
  statItem: {
    backgroundColor: '#c8e6c9',
    padding: '8px 20px',
    borderRadius: '20px',
    color: '#1b5e20',
    fontSize: '1.1rem',
    fontWeight: 'bold',
  },
  exerciseTypeContainer: {
    display: 'flex',
    justifyContent: 'center',
    gap: '15px',
    marginBottom: '30px',
  },
  typeButton: {
    padding: '12px 30px',
    fontSize: '1.1rem',
    border: '2px solid #66bb6a',
    borderRadius: '25px',
    backgroundColor: 'white',
    color: '#2e7d32',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    fontWeight: 'bold',
  },
  typeButtonActive: {
    backgroundColor: '#66bb6a',
    color: 'white',
  },
  exerciseCard: {
    maxWidth: '600px',
    margin: '0 auto',
    backgroundColor: 'white',
    borderRadius: '20px',
    padding: '40px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  questionContainer: {
    marginBottom: '30px',
  },
  question: {
    fontSize: '2rem',
    color: '#2e7d32',
    textAlign: 'center',
    marginBottom: '20px',
  },
  timerContainer: {
    width: '100%',
    height: '8px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
    overflow: 'hidden',
    marginTop: '15px',
  },
  timerBar: {
    height: '100%',
    backgroundColor: '#81c784',
    transition: 'width 1s linear',
  },
  answerContainer: {
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    padding: '15px',
    fontSize: '1.3rem',
    border: '2px solid #a5d6a7',
    borderRadius: '10px',
    outline: 'none',
    backgroundColor: '#f1f8f4',
  },
  submitButton: {
    padding: '15px 30px',
    fontSize: '1.2rem',
    backgroundColor: '#66bb6a',
    color: 'white',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    fontWeight: 'bold',
    transition: 'all 0.3s ease',
  },
  feedbackContainer: {
    textAlign: 'center',
    padding: '20px',
  },
  feedback: {
    fontSize: '1.8rem',
    color: '#2e7d32',
    fontWeight: 'bold',
  },
  encouragement: {
    textAlign: 'center',
    marginTop: '30px',
  },
  encouragementText: {
    fontSize: '1.2rem',
    color: '#388e3c',
    fontWeight: '500',
  },
};

export default App;
