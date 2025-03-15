import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ComponentListTemplate from '../components/templates/ComponentListTemplate';
import ComponentDetailTemplate from '../components/templates/ComponentDetailTemplate';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';

/**
 * Creates both list and detail page components for a component type with
 * integrated loading states and error handling.
 *
 * @param {Object} config - Configuration object
 * @param {string} config.type - The type of component (antennas, cameras, etc.)
 * @param {Function} config.fetchList - Function to fetch the list data
 * @param {Function} config.fetchDetail - Function to fetch the detail data
 * @param {Function} config.renderListItem - Custom renderer for list items (optional)
 * @param {Function} config.renderDetailContent - Function to render component-specific details
 * @param {string} config.title - Optional custom title (defaults to capitalized type)
 * @returns {Object} - Object containing ListPage and DetailPage components
 */
export function createComponentPages(config) {
  const {
    type,
    fetchList,
    fetchDetail,
    renderListItem,
    renderDetailContent,
    title = type.charAt(0).toUpperCase() + type.slice(1)
  } = config;

  /**
   * List page component with integrated state management
   */
  const ListPage = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Function to load the data
    const loadData = async (filterOptions = {}) => {
      try {
        setLoading(true);
        setError(null);

        const result = await fetchList(filterOptions);
        setData(result.results || result);
      } catch (err) {
        console.error(`Error fetching ${type} list:`, err);
        setError(`Failed to load ${type}. ${err.message || 'Please try again later.'}`);
      } finally {
        setLoading(false);
      }
    };

    // Load data on component mount
    useEffect(() => {
      loadData();

      // Cleanup function
      return () => {
        // Any cleanup if needed
      };
    }, []);

    // Show loading spinner while initially loading
    if (loading && !data) {
      return <LoadingSpinner />;
    }

    // Show error message with retry button if request failed
    if (error) {
      return <ErrorMessage message={error} onRetry={loadData} />;
    }

    // Render the list template with data
    return (
      <ComponentListTemplate
        title={title}
        componentType={type}
        items={data || []}
        renderItem={renderListItem}
        isRefreshing={loading && data} // Pass refreshing state separately
        onRefresh={loadData}
      />
    );
  };

  /**
   * Detail page component with integrated state management
   */
  const DetailPage = () => {
    const { id } = useParams(); // Get ID from the URL
    const [item, setItem] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Function to load the detail data
    const loadItem = async () => {
      try {
        setLoading(true);
        setError(null);

        const result = await fetchDetail(id);
        setItem(result);
      } catch (err) {
        console.error(`Error fetching ${type} detail:`, err);
        setError(`Failed to load ${type} details. ${err.message || 'Please try again later.'}`);
      } finally {
        setLoading(false);
      }
    };

    // Load data on component mount or when ID changes
    useEffect(() => {
      loadItem();

      // Cleanup function
      return () => {
        // Any cleanup if needed
      };
    }, [id]);

    // Show loading spinner while loading
    if (loading && !item) {
      return <LoadingSpinner />;
    }

    // Show error message with retry button if request failed
    if (error) {
      return <ErrorMessage message={error} onRetry={loadItem} />;
    }

    // Show not found message if no item was returned
    if (!item) {
      return <ErrorMessage message={`${title} not found.`} />;
    }

    // Render the detail template with data
    return (
      <ComponentDetailTemplate
        componentType={type}
        item={item}
        renderDetails={renderDetailContent}
        isRefreshing={loading && item} // Pass refreshing state separately
        onRefresh={loadItem}
      />
    );
  };

  return { ListPage, DetailPage };
}

/**
 * @deprecated Use createComponentPages instead
 */
export function createComponentListPage(componentType, title, fetchDataFn, renderItemFn) {
  console.warn('createComponentListPage is deprecated, use createComponentPages instead');

  const { ListPage } = createComponentPages({
    type: componentType,
    title: title,
    fetchList: fetchDataFn,
    fetchDetail: () => {}, // No-op because we don't need detail for list
    renderListItem: renderItemFn,
    renderDetailContent: () => null // No-op for detail content
  });

  return ListPage;
}

/**
 * @deprecated Use createComponentPages instead
 */
export function createComponentDetailPage(componentType, fetchDataFn, renderDetailsFn) {
  console.warn('createComponentDetailPage is deprecated, use createComponentPages instead');

  const { DetailPage } = createComponentPages({
    type: componentType,
    fetchList: () => {}, // No-op because we don't need list for detail
    fetchDetail: fetchDataFn,
    renderDetailContent: renderDetailsFn
  });

  return DetailPage;
}