import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';

/**
 * A reusable template for displaying details of any component type
 * 
 * @param {Object} props - Component properties
 * @param {string} props.componentType - Type of component (antennas, cameras, etc.)
 * @param {Function} props.fetchData - Function to fetch the component data
 * @param {Function} props.renderDetails - Function to render the specific details section
 */
function ComponentDetailTemplate({ componentType, fetchData, renderDetails }) {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch component details using provided fetch function
    fetchData(id)
      .then(data => {
        setItem(data);
        setLoading(false);
      })
      .catch(error => {
        console.error(`Error fetching ${componentType} details:`, error);
        setError(`Failed to load ${componentType} details. Please try again later.`);
        setLoading(false);
      });
  }, [fetchData, id, componentType]);

  if (loading) return <div>Loading {componentType} details...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!item) return <div>{componentType} not found</div>;

  return (
    <div className="component-detail">
      <h1>{item.manufacturer} {item.model}</h1>
      <Link to={`/components/${componentType}`}>Back to {componentType}</Link>
      
      <div>
        <h2>Details</h2>
        <p><strong>Description:</strong> {item.description || 'No description available'}</p>
        
        {/* Render component-specific details using the provided function */}
        {renderDetails(item)}
        
        {/* Images section - common to all components */}
        <h3>Images</h3>
        {item.images && item.images.length > 0 ? (
          <div className="component-images">
            {item.images.map((image, index) => (
              <img 
                key={index} 
                src={image.image} 
                alt={`${item.manufacturer} ${item.model}`} 
                className="component-image"
              />
            ))}
          </div>
        ) : (
          <p>No images available</p>
        )}
      </div>
    </div>
  );
}

export default ComponentDetailTemplate;
