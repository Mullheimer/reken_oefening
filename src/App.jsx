import { useState } from 'react';
import Exercise from './components/Exercise';
import SessionSummary from './components/SessionSummary';
import './App.css';

/**
 * Main App Component for Reken Oefening
 * An adaptive learning app for math practice (group 5 level)
 */
function App() {
  const [view, setView] = useState('start'); // 'start', 'exercise', 'summary'
  const [sessionResults, setSessionResults] = useState(null);

  const handleStartExercise = () => {
    setView('exercise');
    setSessionResults(null);
  };

  const handleSessionComplete = (results) => {
    setSessionResults(results);
    setView('summary');
  };

  const handleNewSession = () => {
    setView('exercise');
    setSessionResults(null);
  };

  // Start screen
  if (view === 'start') {
    return (
      <div className="app">
        <div className="start-screen">
          <h1 className="app-title">Reken Oefening</h1>
          <p className="app-subtitle">Leer rekenen op een leuke manier!</p>
          
          <div className="mode-info">
            <span className="mode-icon">➕ ➖</span>
            <span className="mode-text">Optellen en aftrekken tot 20</span>
          </div>
          
          <button 
            className="start-button"
            onClick={handleStartExercise}
            type="button"
          >
            Start met oefenen! 🚀
          </button>
        </div>
      </div>
    );
  }

  // Exercise view
  if (view === 'exercise') {
    return (
      <div className="app">
        <Exercise onSessionComplete={handleSessionComplete} />
      </div>
    );
  }

  // Summary view
  if (view === 'summary') {
    return (
      <div className="app">
        <SessionSummary 
          results={sessionResults} 
          onStartNew={handleNewSession} 
        />
      </div>
    );
  }

  return null;
}

export default App;
