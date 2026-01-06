import { useCallback } from 'react';
import './NumericKeypad.css';

/**
 * NumericKeypad component - A large, touch-friendly numeric keypad for tablet input
 * Designed with accessibility and child-friendliness in mind
 */
const NumericKeypad = ({ onNumberPress, onClear, onSubmit, disabled = false }) => {
  const handleKeyPress = useCallback((value) => {
    if (disabled) return;
    onNumberPress(value);
  }, [disabled, onNumberPress]);

  const handleClear = useCallback(() => {
    if (disabled) return;
    onClear();
  }, [disabled, onClear]);

  const handleSubmit = useCallback(() => {
    if (disabled) return;
    onSubmit();
  }, [disabled, onSubmit]);

  // Keyboard numbers layout
  const numbers = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    [0]
  ];

  return (
    <div className="numeric-keypad" role="group" aria-label="Numeriek toetsenbord">
      <div className="keypad-grid">
        {numbers.map((row, rowIndex) => (
          <div key={rowIndex} className="keypad-row">
            {row.map((num) => (
              <button
                key={num}
                className={`keypad-button number-button ${num === 0 ? 'wide' : ''}`}
                onClick={() => handleKeyPress(num.toString())}
                disabled={disabled}
                type="button"
                aria-label={`Nummer ${num}`}
              >
                {num}
              </button>
            ))}
          </div>
        ))}
        <div className="keypad-row action-row">
          <button
            className="keypad-button clear-button"
            onClick={handleClear}
            disabled={disabled}
            type="button"
            aria-label="Wissen"
          >
            ⌫
          </button>
          <button
            className="keypad-button submit-button"
            onClick={handleSubmit}
            disabled={disabled}
            type="button"
            aria-label="Controleren"
          >
            ✓
          </button>
        </div>
      </div>
    </div>
  );
};

export default NumericKeypad;
