import './SessionSummary.css';

/**
 * SessionSummary component - Shows a positive summary after completing a practice session
 * Focuses on encouragement and celebrating achievements
 */
const SessionSummary = ({ results, onStartNew }) => {
  const { totalCorrect, totalAttempted } = results;
  
  // Calculate percentage (avoid division by zero)
  const percentage = totalAttempted > 0 
    ? Math.round((totalCorrect / totalAttempted) * 100) 
    : 0;

  // Get encouraging message based on performance
  const getEncouragingMessage = () => {
    if (totalAttempted === 0) {
      return 'Probeer het de volgende keer! 🌱';
    }
    if (percentage >= 90) {
      return 'Wauw, wat ben jij goed! 🌟';
    }
    if (percentage >= 70) {
      return 'Heel knap gedaan! 💪';
    }
    if (percentage >= 50) {
      return 'Goed geoefend! 🌈';
    }
    return 'Oefening baart kunst! 🌱';
  };

  // Get star rating (1-5 stars)
  const getStarRating = () => {
    if (totalAttempted === 0) return 1;
    if (percentage >= 90) return 5;
    if (percentage >= 75) return 4;
    if (percentage >= 60) return 3;
    if (percentage >= 40) return 2;
    return 1;
  };

  return (
    <div className="session-summary">
      <div className="summary-card">
        <h2 className="summary-title">Goed gedaan! 🎉</h2>
        
        {/* Stars */}
        <div className="stars-container">
          {Array.from({ length: 5 }, (_, i) => (
            <span 
              key={i} 
              className={`star ${i < getStarRating() ? 'filled' : 'empty'}`}
            >
              ⭐
            </span>
          ))}
        </div>

        {/* Main stats */}
        <div className="main-stat">
          <span className="stat-number">{totalCorrect}</span>
          <span className="stat-label">sommen goed!</span>
        </div>

        {/* Encouraging message */}
        <p className="encouraging-message">{getEncouragingMessage()}</p>

        {/* Additional stats (subtle) */}
        <div className="additional-stats">
          <span>Je hebt {totalAttempted} sommen geprobeerd</span>
        </div>

        {/* Action button */}
        <button 
          className="new-session-button"
          onClick={onStartNew}
          type="button"
        >
          Nog een keer oefenen! 🚀
        </button>
      </div>
    </div>
  );
};

export default SessionSummary;
