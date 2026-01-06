import { useState, useEffect, useCallback } from 'react';
import NumericKeypad from './NumericKeypad';
import { generateMixedSum, checkAnswer, getDifficultyByStreak } from '../utils/sumGenerator';
import './Exercise.css';

// Generate initial sum outside of component to avoid setState in effect
const getInitialSum = () => {
  const difficulty = getDifficultyByStreak(0);
  return generateMixedSum(difficulty.max);
};

/**
 * Exercise component - Main exercise interface for practicing math
 * Features adaptive difficulty and gentle error handling
 */
const Exercise = ({ onSessionComplete }) => {
  const [currentSum, setCurrentSum] = useState(getInitialSum);
  const [userAnswer, setUserAnswer] = useState('');
  const [streak, setStreak] = useState(0);
  const [totalCorrect, setTotalCorrect] = useState(0);
  const [totalAttempted, setTotalAttempted] = useState(0);
  const [feedback, setFeedback] = useState({ show: false, type: '', message: '' });
  const [showCorrectAnswer, setShowCorrectAnswer] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [missedSums, setMissedSums] = useState([]); // Track missed sums to retry later

  // Get encouraging message based on streak
  const getPositiveMessage = useCallback((currentStreak) => {
    const messages = {
      1: ['Goed zo! 👍', 'Prima! ⭐', 'Super! 🌟'],
      2: ['Knap! 🌈', 'Ga zo door! 💪', 'Heel goed! ✨'],
      3: ['Fantastisch! 🎉', 'Geweldig! 🌟', 'Wat knap! 🏆'],
      high: ['Ongelofelijk! 🚀', 'Je bent een ster! ⭐', 'Schitterend! 💎']
    };

    const msgArray = currentStreak >= 3 ? messages.high : messages[currentStreak] || messages[1];
    return msgArray[Math.floor(Math.random() * msgArray.length)];
  }, []);

  // Generate new sum based on current difficulty
  const generateNewSum = useCallback((currentStreak) => {
    const difficulty = getDifficultyByStreak(currentStreak);
    const newSum = generateMixedSum(difficulty.max);
    setCurrentSum(newSum);
    setUserAnswer('');
    setShowCorrectAnswer(false);
    setFeedback({ show: false, type: '', message: '' });
  }, []);

  // Handle number button press
  const handleNumberPress = useCallback((num) => {
    if (isProcessing || showCorrectAnswer) return;
    // Limit to 3 digits (max answer is 20)
    setUserAnswer(prev => {
      if (prev.length < 3) {
        return prev + num;
      }
      return prev;
    });
  }, [isProcessing, showCorrectAnswer]);

  // Handle clear button
  const handleClear = useCallback(() => {
    if (isProcessing || showCorrectAnswer) return;
    setUserAnswer(prev => prev.slice(0, -1));
  }, [isProcessing, showCorrectAnswer]);

  // Handle submit/check answer
  const handleSubmit = useCallback(async () => {
    if (!userAnswer || !currentSum || isProcessing || showCorrectAnswer) return;
    
    setIsProcessing(true);
    setTotalAttempted(prev => prev + 1);

    const isCorrect = checkAnswer(currentSum, userAnswer);

    if (isCorrect) {
      // Correct answer - positive feedback
      setStreak(prev => {
        const newStreak = prev + 1;
        setFeedback({
          show: true,
          type: 'correct',
          message: getPositiveMessage(newStreak)
        });
        
        // Brief pause before next sum
        setTimeout(() => {
          generateNewSum(newStreak);
          setIsProcessing(false);
        }, 800);
        
        return newStreak;
      });
      setTotalCorrect(prev => prev + 1);
    } else {
      // Incorrect - show correct answer gently
      setStreak(0); // Reset streak
      setShowCorrectAnswer(true);
      setFeedback({
        show: true,
        type: 'incorrect',
        message: `Het goede antwoord is ${currentSum.correctAnswer}`
      });
      
      // Add to missed sums for later retry
      setMissedSums(prev => [...prev, currentSum]);
      
      // Longer pause to let child see the correct answer
      setTimeout(() => {
        generateNewSum(0);
        setIsProcessing(false);
      }, 2000);
    }
  }, [userAnswer, currentSum, isProcessing, showCorrectAnswer, getPositiveMessage, generateNewSum]);

  // Handle keyboard input from physical keyboard
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Number keys
      if (e.key >= '0' && e.key <= '9') {
        handleNumberPress(e.key);
      }
      // Backspace
      else if (e.key === 'Backspace') {
        handleClear();
      }
      // Enter
      else if (e.key === 'Enter') {
        handleSubmit();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleNumberPress, handleClear, handleSubmit]);

  // Handle session end
  const handleEndSession = () => {
    onSessionComplete({
      totalCorrect,
      totalAttempted,
      missedSums
    });
  };

  // Get current difficulty name
  const getCurrentDifficulty = () => {
    return getDifficultyByStreak(streak).name;
  };

  return (
    <div className="exercise-container">
      {/* Progress indicator */}
      <div className="progress-info">
        <span className="correct-count">{totalCorrect} goed</span>
        <span className="difficulty-badge">{getCurrentDifficulty()}</span>
      </div>

      {/* Streak indicator (only show when in flow) */}
      {streak >= 2 && (
        <div className="streak-indicator">
          {Array.from({ length: Math.min(streak, 5) }, (_, i) => (
            <span key={i} className="streak-star">⭐</span>
          ))}
        </div>
      )}

      {/* Main sum display */}
      <div className="sum-display">
        <div className="sum-numbers">
          <span className="number">{currentSum.num1}</span>
          <span className="operator">{currentSum.operation}</span>
          <span className="number">{currentSum.num2}</span>
          <span className="equals">=</span>
          <span className={`answer ${showCorrectAnswer ? 'show-correct' : ''}`}>
            {showCorrectAnswer ? currentSum.correctAnswer : (userAnswer || '?')}
          </span>
        </div>
      </div>

      {/* Feedback message */}
      {feedback.show && (
        <div className={`feedback ${feedback.type}`}>
          {feedback.message}
        </div>
      )}

      {/* Numeric keypad */}
      <NumericKeypad
        onNumberPress={handleNumberPress}
        onClear={handleClear}
        onSubmit={handleSubmit}
        disabled={isProcessing}
      />

      {/* End session button */}
      <button 
        className="end-session-button"
        onClick={handleEndSession}
        type="button"
      >
        Klaar met oefenen
      </button>
    </div>
  );
};

export default Exercise;
