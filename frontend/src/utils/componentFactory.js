import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation, useSearchParams } from 'react-router-dom';
import ComponentListTemplate from '../components/templates/ComponentListTemplate';
import ComponentDetailTemplate from '../components/templates/ComponentDetailTemplate';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';
import { getKeySpecsForComponentType, generateComponentTags } from '../config/componentSpecs';

/**
 * Creates both list and detail page components for a component type with
 * integrated state management, pagination, and sorting.
 *
 * @param {Object} config - Configuration object
 * @param {string} config.type - The type of component (antennas, cameras, etc.)
 * @param {Function} config.fetchList - Function to fetch the list data
 * @param {Function} config.fetchDetail - Function to fetch the detail data
 * @param {string} config.title - Optional custom title (defaults to capitalized type)
 * @param {Node} config.filterSidebar - Optional filter sidebar component
 * @returns {Object} - Object containing ListPage and DetailPage components
 */
export function createComponentPages(config) {
  const {
    type,
    fetchList,
    fetchDetail,
    title = type.charAt(0).toUpperCase() + type.slice(1),
    filterSidebar
  } = config;

  /**
   * Enhanced list page component with integrated state management,
   * pagination, sorting, and view mode
   */
  const ListPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();

    // Get current page from URL or default to 1
    const page = parseInt(searchParams.get('page') || '1', 10);

    // Get current sort from URL or default
    const sort = searchParams.get('sort') || 'name-asc';

    // Get filter params, excluding page and sort
    const filterParams = {};
    searchParams.forEach((value, key) => {
      if (key !== 'page' && key !== 'sort') {
        filterParams[key] = value;
      }
    });

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({
      page: page,
      totalPages: 1,
      totalCount: 0,
    });

    // Function to load the data
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Build params object with pagination, sorting, and filters
        const params = {
          page: page,
          ...filterParams
        };

        // Add sorting parameters based on sort value
        if (sort === 'name-asc') {
          params.ordering = 'manufacturer,model';
        } else if (sort === 'name-desc') {
          params.ordering = '-manufacturer,-model';
        } else if (sort === 'newest') {
          params.ordering = '-created_at';
        } else if (sort === 'oldest') {
          params.ordering = 'created_at';
        }

        const result = await fetchList(params);

        // Pre-process items to add tags
        const items = (result.results || result).map(item => ({
          ...item,
          tags: generateComponentTags(type, item)
        }));

        setData(items);

        // Set pagination info from API response or defaults
        if (result.count !== undefined) {
          setPagination({
            page: page,
            totalPages: Math.ceil(result.count / (result.page_size || 36)),
            totalCount: result.count
          });
        }
      } catch (err) {
        console.error(`Error fetching ${type} list:`, err);
        setError(`Failed to load ${type}. ${err.message || 'Please try again later.'}`);
      } finally {
        setLoading(false);
      }
    };

    // Handle page change
    const handlePageChange = (newPage) => {
      searchParams.set('page', newPage.toString());
      setSearchParams(searchParams);
    };

    // Handle sort change
    const handleSortChange = (newSort) => {
      searchParams.set('sort', newSort);
      setSearchParams(searchParams);
    };

    // Load data when parameters change
    useEffect(() => {
      loadData();
    }, [page, sort, JSON.stringify(filterParams)]);

    // Show loading spinner while initially loading
    if (loading && !data) {
      return <LoadingSpinner />;
    }

    // Show error message with retry button if request failed
    if (error) {
      return <ErrorMessage message={error} onRetry={loadData} />;
    }

    // Get the component-specific specifications
    const specsConfig = getKeySpecsForComponentType(type);

    // Render the list template with data
    return (
      <ComponentListTemplate
        title={title}
        componentType={type}
        items={data || []}
        pagination={pagination}
        onPageChange={handlePageChange}
        sortBy={sort}
        onSortChange={handleSortChange}
        isRefreshing={loading && data} // Pass refreshing state separately
        onRefresh={loadData}
        specsConfig={specsConfig}
        filterSidebar={filterSidebar}
      />
    );
  };

  /**
   * Enhanced detail page component with integrated state management
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

        // Add tags to the item
        setItem({
          ...result,
          tags: generateComponentTags(type, result)
        });
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

    // Get the component-specific specifications
    const specsConfig = getKeySpecsForComponentType(type);

    // Render the detail template with data
    return (
      <ComponentDetailTemplate
        componentType={type}
        item={item}
        renderDetails={() => renderDetailContent(item, specsConfig)}
        isRefreshing={loading && item} // Pass refreshing state separately
        onRefresh={loadItem}
      />
    );
  };

  return { ListPage, DetailPage };
}

/**
 * Helper function to render component details
 * This can be customized based on the component type
 */
function renderDetailContent(item, specsConfig) {
  // Implementation will be updated when we focus on details page
  return (
    <div>
      {/* This is a placeholder. We'll implement a proper detail view later */}
      <pre>{JSON.stringify(item, null, 2)}</pre>
    </div>
  );
}
