/**
 * Sum Generator for math exercises
 * Generates addition and subtraction problems with configurable difficulty levels
 */

// Difficulty levels for the adaptive algorithm
export const DIFFICULTY_LEVELS = {
  EASY: { max: 10, name: 'Makkelijk' },
  MEDIUM: { max: 15, name: 'Gemiddeld' },
  HARD: { max: 20, name: 'Moeilijk' }
};

// Operation types
export const OPERATIONS = {
  ADDITION: '+',
  SUBTRACTION: '-'
};

/**
 * Generate a random integer between min and max (inclusive)
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Random integer
 */
const getRandomInt = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

/**
 * Generate a single math sum based on difficulty settings
 * @param {string} operation - Operation type ('+' or '-')
 * @param {number} maxNumber - Maximum number for the sum (minimum 2)
 * @returns {Object} Sum object with num1, num2, operation, and correctAnswer
 */
export const generateSum = (operation = OPERATIONS.ADDITION, maxNumber = 10) => {
  // Ensure maxNumber is at least 2 for valid sums
  const safeMax = Math.max(maxNumber, 2);
  let num1, num2, correctAnswer;

  if (operation === OPERATIONS.ADDITION) {
    // For addition, ensure the sum doesn't exceed maxNumber
    num1 = getRandomInt(1, safeMax - 1);
    num2 = getRandomInt(1, safeMax - num1);
    correctAnswer = num1 + num2;
  } else {
    // For subtraction, ensure the result is non-negative
    num1 = getRandomInt(2, safeMax);
    num2 = getRandomInt(1, num1);
    correctAnswer = num1 - num2;
  }

  return {
    id: crypto.randomUUID(),
    num1,
    num2,
    operation,
    correctAnswer,
    displayText: `${num1} ${operation} ${num2} = ?`
  };
};

/**
 * Generate a mixed sum (randomly chosen addition or subtraction)
 * @param {number} maxNumber - Maximum number for the sum
 * @returns {Object} Sum object
 */
export const generateMixedSum = (maxNumber = 10) => {
  const operation = Math.random() > 0.5 ? OPERATIONS.ADDITION : OPERATIONS.SUBTRACTION;
  return generateSum(operation, maxNumber);
};

/**
 * Generate a batch of sums
 * @param {number} count - Number of sums to generate
 * @param {string} mode - 'addition', 'subtraction', or 'mixed'
 * @param {number} maxNumber - Maximum number for the sums
 * @returns {Array} Array of sum objects
 */
export const generateSumBatch = (count = 10, mode = 'mixed', maxNumber = 10) => {
  const sums = [];
  
  for (let i = 0; i < count; i++) {
    let sum;
    switch (mode) {
      case 'addition':
        sum = generateSum(OPERATIONS.ADDITION, maxNumber);
        break;
      case 'subtraction':
        sum = generateSum(OPERATIONS.SUBTRACTION, maxNumber);
        break;
      case 'mixed':
      default:
        sum = generateMixedSum(maxNumber);
        break;
    }
    sums.push(sum);
  }
  
  return sums;
};

/**
 * Get difficulty level based on consecutive correct answers
 * @param {number} streak - Number of consecutive correct answers
 * @returns {Object} Difficulty level object
 */
export const getDifficultyByStreak = (streak) => {
  if (streak >= 6) {
    return DIFFICULTY_LEVELS.HARD;
  } else if (streak >= 3) {
    return DIFFICULTY_LEVELS.MEDIUM;
  }
  return DIFFICULTY_LEVELS.EASY;
};

/**
 * Check if an answer is correct
 * @param {Object} sum - The sum object
 * @param {number} answer - The provided answer
 * @returns {boolean} True if correct
 */
export const checkAnswer = (sum, answer) => {
  return sum.correctAnswer === parseInt(answer, 10);
};
