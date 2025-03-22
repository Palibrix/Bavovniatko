import React, { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight, faPlus, faMinus, faExpand, faCompress, faTimes } from '@fortawesome/free-solid-svg-icons';
import { themeClasses } from '../../utils/themeUtils';

/**
 * Component gallery with main image, thumbnails, navigation, and fullscreen mode
 *
 * @param {Object} props Component properties
 * @param {Array} props.images Array of image objects
 * @param {string} props.alt Alt text for images
 * @param {string} props.themeClass Theme color for styling
 */
const ComponentGallery = ({ images = [], alt = 'Component image', themeClass }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [imagePosition, setImagePosition] = useState({ x: 0, y: 0 });

  const mainImageRef = useRef(null);
  const galleryContainerRef = useRef(null);

  // Fallback image if no images are provided
  const placeholderImage = '/api/placeholder/400/300';

  // Get the current image or placeholder
  const currentImage = images && images.length > 0
    ? images[currentIndex]?.image || placeholderImage
    : placeholderImage;

  // Navigate to previous image
  const prevImage = () => {
    if (!images || images.length <= 1) return;
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? images.length - 1 : prevIndex - 1));
    resetImageView();
  };

  // Navigate to next image
  const nextImage = () => {
    if (!images || images.length <= 1) return;
    setCurrentIndex((prevIndex) => (prevIndex === images.length - 1 ? 0 : prevIndex + 1));
    resetImageView();
  };

  // Select a specific image by index
  const selectImage = (index) => {
    if (index >= 0 && index < images.length) {
      setCurrentIndex(index);
      resetImageView();
    }
  };

  // Zoom controls
  const zoomIn = () => {
    setZoomLevel(prev => Math.min(prev + 0.5, 3));
  };

  const zoomOut = () => {
    if (zoomLevel <= 1) {
      resetImageView();
    } else {
      setZoomLevel(prev => Math.max(prev - 0.5, 1));
    }
  };

  const resetZoom = () => {
    resetImageView();
  };

  // Reset all image view properties
  const resetImageView = () => {
    setZoomLevel(1);
    setImagePosition({ x: 0, y: 0 });
  };

  // Toggle fullscreen mode
  const toggleFullscreen = () => {
    if (!isFullscreen) {
      if (galleryContainerRef.current && galleryContainerRef.current.requestFullscreen) {
        galleryContainerRef.current.requestFullscreen()
          .then(() => setIsFullscreen(true))
          .catch(err => console.error(`Fullscreen error: ${err.message}`));
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen()
          .then(() => setIsFullscreen(false))
          .catch(err => console.error(`Exit fullscreen error: ${err.message}`));
      }
    }
  };

  // Update fullscreen state when fullscreen changes from browser controls
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  // Mouse events for dragging/panning
  const handleMouseDown = (e) => {
    // Only enable dragging when zoomed in
    if (zoomLevel > 1) {
      e.preventDefault(); // Prevent browser's default drag behavior
      setIsDragging(true);
      setDragStart({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging && zoomLevel > 1) {
      e.preventDefault(); // Prevent selection during drag
      const dx = e.clientX - dragStart.x;
      const dy = e.clientY - dragStart.y;

      // Calculate boundaries to prevent dragging too far
      const maxX = (zoomLevel - 1) * (mainImageRef.current?.clientWidth || 0) / 2;
      const maxY = (zoomLevel - 1) * (mainImageRef.current?.clientHeight || 0) / 2;

      // Update position with constraints
      setImagePosition(prev => ({
        x: Math.max(-maxX, Math.min(maxX, prev.x + dx)),
        y: Math.max(-maxY, Math.min(maxY, prev.y + dy))
      }));

      setDragStart({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Touch events for mobile
  const handleTouchStart = (e) => {
    if (e.touches.length === 1 && zoomLevel > 1) {
      e.preventDefault();
      setIsDragging(true);
      setDragStart({ x: e.touches[0].clientX, y: e.touches[0].clientY });
    }
  };

  const handleTouchMove = (e) => {
    if (isDragging && zoomLevel > 1 && e.touches.length === 1) {
      e.preventDefault(); // Prevent scrolling
      const dx = e.touches[0].clientX - dragStart.x;
      const dy = e.touches[0].clientY - dragStart.y;

      // Calculate boundaries to prevent dragging too far
      const maxX = (zoomLevel - 1) * (mainImageRef.current?.clientWidth || 0) / 2;
      const maxY = (zoomLevel - 1) * (mainImageRef.current?.clientHeight || 0) / 2;

      // Update position with constraints
      setImagePosition(prev => ({
        x: Math.max(-maxX, Math.min(maxX, prev.x + dx)),
        y: Math.max(-maxY, Math.min(maxY, prev.y + dy))
      }));

      setDragStart({ x: e.touches[0].clientX, y: e.touches[0].clientY });
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
  };

  return (
    <div>
      {/* Main image container */}
      <div
        ref={galleryContainerRef}
        className={`bg-white rounded-3xl mb-5 shadow-sm relative overflow-hidden ${isFullscreen ? 'fixed inset-0 z-50 m-0 rounded-none' : 'h-[420px]'}`}
        style={{ touchAction: zoomLevel > 1 ? 'none' : 'auto' }}
      >
        <div
          ref={mainImageRef}
          className={`w-full h-full flex items-center justify-center p-8 transition-transform duration-200 ${
            isFullscreen ? 'p-16' : ''
          } ${isDragging ? 'cursor-grabbing' : zoomLevel > 1 ? 'cursor-grab' : ''}`}
          style={{ userSelect: 'none' }}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          <img
            src={currentImage}
            alt={alt}
            className="max-w-full max-h-full object-contain transition-transform duration-200 ease-out select-none pointer-events-none"
            style={{
              transform: `scale(${zoomLevel}) translate(${imagePosition.x}px, ${imagePosition.y}px)`,
              transformOrigin: 'center center'
            }}
          />
        </div>

        {/* Right accent line - hide in fullscreen */}
        {!isFullscreen && (
          <div className={`absolute top-0 bottom-0 right-0 w-1 bg-gradient-to-b ${themeClass.bg} opacity-80`}></div>
        )}

        {/* Close button in fullscreen mode */}
        {isFullscreen && (
          <button
            onClick={toggleFullscreen}
            className="absolute top-4 right-4 z-20 bg-white bg-opacity-90 rounded-full w-10 h-10 flex items-center justify-center shadow-md text-gray-600 hover:text-gray-900 transition-colors"
            aria-label="Exit fullscreen"
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        )}

        {/* Zoom controls */}
        <div className="absolute top-4 right-4 bg-white bg-opacity-90 rounded-lg shadow-sm flex overflow-hidden z-10">
          <button
            onClick={zoomIn}
            className={`w-8 h-8 flex items-center justify-center hover:bg-opacity-10 hover:${themeClass.bgOpacity[10]} transition-colors`}
            aria-label="Zoom in"
          >
            <FontAwesomeIcon icon={faPlus} className="text-gray-600" />
          </button>
          <button
            onClick={zoomOut}
            className={`w-8 h-8 flex items-center justify-center hover:bg-opacity-10 hover:${themeClass.bgOpacity[10]} transition-colors`}
            aria-label="Zoom out"
          >
            <FontAwesomeIcon icon={faMinus} className="text-gray-600" />
          </button>
          <button
            onClick={resetZoom}
            className={`w-8 h-8 flex items-center justify-center hover:bg-opacity-10 hover:${themeClass.bgOpacity[10]} transition-colors`}
            aria-label="Reset zoom"
          >
            <FontAwesomeIcon icon={faExpand} className="text-gray-600" />
          </button>
          <button
            onClick={toggleFullscreen}
            className={`w-8 h-8 flex items-center justify-center hover:bg-opacity-10 hover:${themeClass.bgOpacity[10]} transition-colors`}
            aria-label={isFullscreen ? "Exit fullscreen" : "Enter fullscreen"}
          >
            <FontAwesomeIcon
              icon={isFullscreen ? faCompress : faExpand}
              className="text-gray-600"
            />
          </button>
        </div>

        {/* Navigation arrows - only show if there are multiple images */}
        {images && images.length > 1 && (
          <div className="absolute top-1/2 left-0 right-0 transform -translate-y-1/2 flex justify-between px-4 z-10">
            <button
              onClick={prevImage}
              className={`w-10 h-10 rounded-full bg-white flex items-center justify-center ${themeClass.border} ${themeClass.text} hover:${themeClass.bg} hover:text-white transition-colors shadow-sm`}
              aria-label="Previous image"
            >
              <FontAwesomeIcon icon={faChevronLeft} />
            </button>
            <button
              onClick={nextImage}
              className={`w-10 h-10 rounded-full bg-white flex items-center justify-center ${themeClass.border} ${themeClass.text} hover:${themeClass.bg} hover:text-white transition-colors shadow-sm`}
              aria-label="Next image"
            >
              <FontAwesomeIcon icon={faChevronRight} />
            </button>
          </div>
        )}
      </div>

      {/* Thumbnails - Don't show in fullscreen mode */}
      {!isFullscreen && images && images.length > 1 && (
        <div className="flex gap-2 mb-6 overflow-x-auto py-1">
          {images.map((image, index) => (
            <button
              key={index}
              onClick={() => selectImage(index)}
              className={`w-16 h-16 flex-shrink-0 bg-white rounded-lg border-2 ${
                index === currentIndex 
                  ? themeClass.border
                  : 'border-transparent hover:border-gray-200'
              } flex items-center justify-center cursor-pointer transition-all hover:-translate-y-1`}
              aria-label={`View image ${index + 1}`}
              aria-current={index === currentIndex ? 'true' : 'false'}
            >
              <img
                src={image.image}
                alt={`${alt} thumbnail ${index + 1}`}
                className="max-w-[80%] max-h-[80%] object-contain"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

ComponentGallery.propTypes = {
  images: PropTypes.arrayOf(
    PropTypes.shape({
      image: PropTypes.string.isRequired,
      order: PropTypes.number
    })
  ),
  alt: PropTypes.string,
  themeColor: PropTypes.string
};

export default ComponentGallery;