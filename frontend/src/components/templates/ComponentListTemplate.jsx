import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

/**
 * A reusable template for displaying lists of any component type
 * 
 * @param {Object} props - Component properties
 * @param {string} props.title - Page title
 * @param {string} props.componentType - Type of component (antennas, cameras, etc.)
 * @param {Function} props.fetchData - Function to fetch the component data
 * @param {Function} props.renderItem - Optional custom render function for list items
 * @param {Object} props.filterOptions - Optional filter options for the API call
 */
function ComponentListTemplate({ 
  title, 
  componentType, 
  fetchData, 
  renderItem,
  filterOptions = {} 
}) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch components using provided fetch function
    fetchData(filterOptions)
      .then(data => {
        setItems(data.results || data);
        setLoading(false);
      })
      .catch(error => {
        console.error(`Error fetching ${componentType} data:`, error);
        setError(`Failed to load ${componentType}. Please try again later.`);
        setLoading(false);
      });
  }, []);

  // Default item renderer if none is provided
  const defaultRenderItem = (item) => (
    <li key={item.id}>
      <Link to={`/components/${componentType}/${item.id}`}>
        {item.manufacturer} {item.model}
      </Link>
    </li>
  );

  // Use the provided renderItem function or fall back to the default
  const renderListItem = renderItem || defaultRenderItem;

  if (loading) return <div>Loading {componentType}...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="component-list">
      <h1>{title}</h1>
      <Link to="/">Back to Home</Link>
      
      <div>
        {items.length === 0 ? (
          <p>No {componentType} found.</p>
        ) : (
          <ul>
            {items.map(item => renderListItem(item))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default ComponentListTemplate;
