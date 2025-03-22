import React from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';

/**
 * Pagination component for navigating between pages of results
 *
 * @param {Object} props Component properties
 * @param {number} props.currentPage Current page number (1-based index)
 * @param {number} props.totalPages Total number of pages
 * @param {Function} props.onPageChange Callback function when page changes
 * @param {number} props.siblingCount Number of siblings to show around current page
 * @param {string} props.themeClass Color class theme for active page
 */
const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
  siblingCount = 1,
  themeClass
}) => {
  if (totalPages <= 1) return null;

  // Generate array of page numbers to display
  const getPageNumbers = () => {
    const totalNumbers = siblingCount * 2 + 3; // siblings + current + first + last
    const totalBlocks = totalNumbers + 2; // +2 for the dots

    if (totalPages <= totalBlocks) {
      // If we have enough space to show all pages
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    const leftSiblingIndex = Math.max(currentPage - siblingCount, 1);
    const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages);

    const showLeftDots = leftSiblingIndex > 2;
    const showRightDots = rightSiblingIndex < totalPages - 1;

    // Always show first and last page
    if (showLeftDots && showRightDots) {
      const middleRange = Array.from(
        { length: rightSiblingIndex - leftSiblingIndex + 1 },
        (_, i) => leftSiblingIndex + i
      );
      return [1, '...', ...middleRange, '...', totalPages];
    }

    if (showLeftDots && !showRightDots) {
      const rightItemCount = 3 + 2 * siblingCount;
      const rightRange = Array.from(
        { length: rightItemCount },
        (_, i) => totalPages - rightItemCount + i + 1
      );
      return [1, '...', ...rightRange];
    }

    if (!showLeftDots && showRightDots) {
      const leftItemCount = 3 + 2 * siblingCount;
      const leftRange = Array.from(
        { length: leftItemCount },
        (_, i) => i + 1
      );
      return [...leftRange, '...', totalPages];
    }

    // Fallback - should never happen
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  };

  const pages = getPageNumbers();

  return (
    <div className="flex justify-center mt-8">
      <div className="flex gap-2">
        {/* Previous button */}
        <button
          className={`min-w-10 h-10 flex items-center justify-center rounded-md border ${
            currentPage === 1 
              ? 'opacity-50 cursor-not-allowed text-gray-400 border-gray-200' 
              : 'border-gray-300 text-gray-700 hover:bg-gray-50'
          }`}
          onClick={() => currentPage > 1 && onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          aria-label="Previous page"
        >
          <FontAwesomeIcon icon={faChevronLeft} />
        </button>

        {/* Page numbers */}
        {pages.map((page, index) => (
          <button
            key={index}
            className={`min-w-10 h-10 flex items-center justify-center rounded-md ${
              page === currentPage
                ? `${themeClass.bg} text-white border ${themeClass.border}`
                : page === '...'
                  ? 'text-gray-500 border border-transparent cursor-default'
                  : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
            onClick={() => page !== '...' && onPageChange(page)}
            disabled={page === '...'}
          >
            {page}
          </button>
        ))}

        {/* Next button */}
        <button
          className={`min-w-10 h-10 flex items-center justify-center rounded-md border ${
            currentPage === totalPages 
              ? 'opacity-50 cursor-not-allowed text-gray-400 border-gray-200' 
              : 'border-gray-300 text-gray-700 hover:bg-gray-50'
          }`}
          onClick={() => currentPage < totalPages && onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          aria-label="Next page"
        >
          <FontAwesomeIcon icon={faChevronRight} />
        </button>
      </div>
    </div>
  );
};

Pagination.propTypes = {
  currentPage: PropTypes.number.isRequired,
  totalPages: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  siblingCount: PropTypes.number,
  themeColor: PropTypes.string
};

export default Pagination;