import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';

/**
 * Reusable dropdown component with Tailwind styling
 *
 * @param {Object} props
 * @param {React.ReactNode} props.trigger - Element that triggers the dropdown
 * @param {React.ReactNode} props.children - Content to show in the dropdown
 * @param {string} props.align - Alignment of dropdown (left, right)
 * @param {string} props.width - Width of dropdown (auto, sm, md, lg, xl)
 * @param {Function} props.onOpen - Callback when dropdown opens
 * @param {Function} props.onClose - Callback when dropdown closes
 */
function Dropdown({
  trigger,
  children,
  align = 'left',
  width = 'md',
  onOpen,
  onClose
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Map width names to actual width classes
  const widthClasses = {
    auto: 'w-auto',
    sm: 'w-48',
    md: 'w-80',
    lg: 'w-80',
    xl: 'w-96'
  };

  // Map alignment to position classes
  const alignmentClasses = {
    left: 'left-0',
    right: 'right-0'
  };

  // Handle click outside to close dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        closeDropdown();
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      // Call onOpen callback if provided
      if (onOpen) onOpen();
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onOpen]);

  // Close with ESC key
  useEffect(() => {
    function handleEscape(event) {
      if (event.key === 'Escape' && isOpen) {
        closeDropdown();
      }
    }

    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen]);

  // Toggle dropdown
  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  // Close dropdown
  const closeDropdown = () => {
    setIsOpen(false);
    if (onClose) onClose();
  };

  return (
    <div ref={dropdownRef} className="relative">
      {/* Trigger element - typically a button */}
      <div
        onClick={toggleDropdown}
        className="cursor-pointer"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        {trigger || (
          <button className="flex items-center text-light-text hover:text-secondary transition-colors">
            Dropdown
            <FontAwesomeIcon
              icon={faChevronDown}
              className={`ml-2 text-xs transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
            />
          </button>
        )}
      </div>

      {/* Dropdown menu */}
      {isOpen && (
        <div
          className={`absolute z-50 mt-2 ${widthClasses[width] || 'w-64'} ${alignmentClasses[align]} bg-white rounded-lg shadow-lg overflow-hidden`}
          role="menu"
          aria-orientation="vertical"
        >
          <div className="py-2">{children}</div>
        </div>
      )}
    </div>
  );
}

/**
 * Dropdown section with a title
 */
export function DropdownSection({ title, children }) {
  return (
    <div className="px-4 py-2">
      {title && <h3 className="text-xs uppercase font-semibold text-gray-500 pb-1 border-b border-gray-100 mb-2">{title}</h3>}
      <div>{children}</div>
    </div>
  );
}

/**
 * Dropdown item - use for links or buttons inside dropdown
 */
export function DropdownItem({ icon, children, onClick, href, className = "" }) {
  const baseClasses = "flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer";

  if (href) {
    return (
      <a href={href} className={`${baseClasses} ${className}`} role="menuitem">
        {icon && <span className="mr-3 text-gray-400">{icon}</span>}
        {children}
      </a>
    );
  }

  return (
    <div
      onClick={onClick}
      className={`${baseClasses} ${className}`}
      role="menuitem"
      tabIndex="0"
    >
      {icon && <span className="mr-3 text-gray-400">{icon}</span>}
      {children}
    </div>
  );
}

/**
 * Dropdown divider line
 */
export function DropdownDivider() {
  return <hr className="my-1 border-gray-100" />;
}

export default Dropdown;