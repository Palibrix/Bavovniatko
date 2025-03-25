import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

/**
 * Toast notification component
 */
const Toast = ({
  message,
  type = 'info',
  duration = 3000,
  onClose
}) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (!message) return;

    const timer = setTimeout(() => {
      setIsVisible(false);
      if (onClose) onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [message, duration, onClose]);

  if (!message || !isVisible) return null;

  // Determine the color based on the type
  const getTypeStyles = () => {
    switch (type) {
      case 'success':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      case 'warning':
        return 'bg-yellow-500';
      default:
        return 'bg-blue-500';
    }
  };

  return (
    <div className={`fixed top-5 right-5 z-50 p-4 rounded-md text-white shadow-md ${getTypeStyles()} transition-all duration-300 transform translate-y-0 opacity-100`}>
      <div className="flex items-center">
        {type === 'success' && <i className="fas fa-check-circle mr-2"></i>}
        {type === 'error' && <i className="fas fa-exclamation-circle mr-2"></i>}
        {type === 'warning' && <i className="fas fa-exclamation-triangle mr-2"></i>}
        {type === 'info' && <i className="fas fa-info-circle mr-2"></i>}
        <span>{message}</span>
        <button
          className="ml-4 text-white hover:text-gray-200"
          onClick={() => {
            setIsVisible(false);
            if (onClose) onClose();
          }}
        >
          <i className="fas fa-times"></i>
        </button>
      </div>
    </div>
  );
};

Toast.propTypes = {
  message: PropTypes.string,
  type: PropTypes.oneOf(['success', 'error', 'warning', 'info']),
  duration: PropTypes.number,
  onClose: PropTypes.func
};

export default Toast;