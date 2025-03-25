import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faCircle } from '@fortawesome/free-solid-svg-icons';

/**
 * Password strength meter with requirements list
 */
const PasswordStrengthMeter = ({ password }) => {
  const [strength, setStrength] = useState(0);
  const [status, setStatus] = useState('Enter password');
  const [meetsLength, setMeetsLength] = useState(false);
  const [meetsUppercase, setMeetsUppercase] = useState(false);
  const [meetsNumber, setMeetsNumber] = useState(false);
  const [meetsSpecial, setMeetsSpecial] = useState(false);

  // Update strength whenever password changes
  useEffect(() => {
    let newStrength = 0;

    // Check length
    if (password.length >= 8) {
      setMeetsLength(true);
      newStrength += 25;
    } else {
      setMeetsLength(false);
    }

    // Check uppercase
    if (/[A-Z]/.test(password)) {
      setMeetsUppercase(true);
      newStrength += 25;
    } else {
      setMeetsUppercase(false);
    }

    // Check numbers
    if (/[0-9]/.test(password)) {
      setMeetsNumber(true);
      newStrength += 25;
    } else {
      setMeetsNumber(false);
    }

    // Check special chars
    if (/[^A-Za-z0-9]/.test(password)) {
      setMeetsSpecial(true);
      newStrength += 25;
    } else {
      setMeetsSpecial(false);
    }

    setStrength(newStrength);

    // Update status text
    if (password.length === 0) {
      setStatus('Enter password');
    } else if (newStrength <= 25) {
      setStatus('Weak');
    } else if (newStrength <= 50) {
      setStatus('Fair');
    } else if (newStrength <= 75) {
      setStatus('Good');
    } else {
      setStatus('Strong');
    }
  }, [password]);

  // Get color based on strength
  const getStrengthColor = () => {
    if (password.length === 0) return '#ddd';
    if (strength <= 25) return '#f09177'; // Error color
    if (strength <= 50) return '#f9c74f'; // Warning
    if (strength <= 75) return '#90be6d'; // Success
    return '#43aa8b'; // Strong success
  };

  return (
    <div className="mt-2">
      <div className="h-1 bg-gray-200 rounded overflow-hidden mb-2">
        <div
          className="h-full rounded transition-all duration-300"
          style={{
            width: `${strength}%`,
            backgroundColor: getStrengthColor()
          }}
        ></div>
      </div>
      <div className="text-xs text-gray-500">Password strength: {status}</div>

      <div className="mt-2 p-3 bg-gray-50 rounded-lg text-sm">
        <div>Password must contain:</div>
        <ul className="mt-2">
          <li className={`mb-1 flex items-center ${meetsLength ? 'text-green-500' : 'text-gray-400'}`}>
            <FontAwesomeIcon icon={meetsLength ? faCheckCircle : faCircle} className="mr-2 text-xs" />
            At least 8 characters
          </li>
          <li className={`mb-1 flex items-center ${meetsUppercase ? 'text-green-500' : 'text-gray-400'}`}>
            <FontAwesomeIcon icon={meetsUppercase ? faCheckCircle : faCircle} className="mr-2 text-xs" />
            At least one uppercase letter
          </li>
          <li className={`mb-1 flex items-center ${meetsNumber ? 'text-green-500' : 'text-gray-400'}`}>
            <FontAwesomeIcon icon={meetsNumber ? faCheckCircle : faCircle} className="mr-2 text-xs" />
            At least one number
          </li>
          <li className={`mb-1 flex items-center ${meetsSpecial ? 'text-green-500' : 'text-gray-400'}`}>
            <FontAwesomeIcon icon={meetsSpecial ? faCheckCircle : faCircle} className="mr-2 text-xs" />
            At least one special character
          </li>
        </ul>
      </div>
    </div>
  );
};

PasswordStrengthMeter.propTypes = {
  password: PropTypes.string.isRequired
};

export default PasswordStrengthMeter;