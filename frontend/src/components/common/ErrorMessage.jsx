import React from 'react';

/**
 * Error message component for displaying API errors
 *
 * @param {Object} props
 * @param {string} props.message - Error message to display
 * @param {Function} props.onRetry - Optional callback for retry button
 */
function ErrorMessage({ message, onRetry }) {
  return (
    <div className="bg-red-50 text-red-700 p-4 rounded-md my-4 border-l-4 border-red-500">
      <div className="flex items-center mb-2">
        <svg
          className="w-5 h-5 mr-2"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clipRule="evenodd"
          />
        </svg>
        <h3 className="font-bold">Error</h3>
      </div>
      <p className="mb-2">{message}</p>

      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 px-4 py-2 bg-white border border-red-500 text-red-600 rounded-md hover:bg-red-50 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
}

export default ErrorMessage;