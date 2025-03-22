import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import {themeClasses} from "../../utils/themeUtils";

/**
 * Expandable/collapsible filter group with smooth animation
 *
 * @param {Object} props Component properties
 * @param {string} props.title Group title
 * @param {boolean} props.initialExpanded Whether the group is initially expanded
 * @param {React.ReactNode} props.children Child components (filter controls)
 * @param {string} props.themeColor Theme color for styling
 */
const FilterGroup = ({ title, initialExpanded = false, children, themeColor = 'primary' }) => {
  const [expanded, setExpanded] = useState(initialExpanded);
  const contentRef = useRef(null);
  const [contentHeight, setContentHeight] = useState(initialExpanded ? 'auto' : '0px');
  const themeClass = themeClasses[themeColor] || themeClasses.primary;

  // Set initial height on mount
  useEffect(() => {
    if (expanded && contentRef.current) {
      setContentHeight(`${contentRef.current.scrollHeight}px`);
    }
  }, []);

  // Handle expansion state change
  useEffect(() => {
    if (!contentRef.current) return;

    if (expanded) {
      // Get the scrollHeight and set it as the height for animation
      const height = contentRef.current.scrollHeight;
      setContentHeight(`${height}px`);

      // After animation completes, set height to auto to accommodate dynamic content
      const timer = setTimeout(() => {
        setContentHeight('auto');
      }, 300); // Should match transition duration

      return () => clearTimeout(timer);
    } else {
      // Set exact height first, then animate to 0
      setContentHeight(`${contentRef.current.scrollHeight}px`);

      // Trigger reflow (using void to indicate intentional side effect)
      void contentRef.current.offsetHeight;

      // Now set height to 0 to animate closed
      setContentHeight('0px');
    }
  }, [expanded]);

  // Handle expand/collapse click
  const toggleExpanded = () => {
    setExpanded((prev) => !prev);
  };

  return (
    <div className="border-b border-gray-100">
      <div
        className="p-4 flex justify-between items-center cursor-pointer transition-colors hover:bg-gray-50"
        onClick={toggleExpanded}
      >
        <h3 className="font-semibold text-gray-700">{title}</h3>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-gray-400 transition-transform duration-300 ${expanded ? 'rotate-180 ' + themeClass.text : ''}`}
        />
      </div>

      <div
        ref={contentRef}
        className="overflow-hidden transition-all duration-300 ease-in-out"
        style={{ height: contentHeight }}
      >
        <div className="p-4 pt-1 pb-5">
          {children}
        </div>
      </div>
    </div>
  );
};

FilterGroup.propTypes = {
  title: PropTypes.string.isRequired,
  initialExpanded: PropTypes.bool,
  children: PropTypes.node.isRequired,
  themeColor: PropTypes.string
};

export default FilterGroup;