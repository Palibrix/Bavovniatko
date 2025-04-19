import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faEdit } from '@fortawesome/free-solid-svg-icons';
import { listsApi } from '../../services/api';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import ErrorMessage from '../../components/common/ErrorMessage';
import ListDetailHeader from '../../components/lists/ListDetailHeader';
import ComponentTypeFilter from '../../components/lists/ComponentTypeFilter';
import ListItemGrid from '../../components/lists/ListItemGrid';
import { ROUTES } from '../../routes';

/**
 * Detail page for a specific list
 */
const ListDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [list, setList] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeType, setActiveType] = useState('all');
  const [viewMode, setViewMode] = useState('list');
  const [sortBy, setSortBy] = useState('newest');
  const [filteredItems, setFilteredItems] = useState([]);

  // Fetch list data
  useEffect(() => {
    fetchListData();
  }, [id]);

  // Filter items when activeType changes
  useEffect(() => {
    if (!list) return;

    filterItemsByType(activeType);
  }, [activeType, list]);

  const fetchListData = async () => {
    try {
      setLoading(true);
      const data = await listsApi.getListById(id);
      setList(data);
      filterItemsByType(activeType);
    } catch (err) {
      console.error('Error fetching list:', err);
      setError(err.message || 'Failed to load list');
    } finally {
      setLoading(false);
    }
  };

  const filterItemsByType = (type) => {
    if (!list || !list.items) {
      setFilteredItems([]);
      return;
    }

    if (type === 'all') {
      setFilteredItems(list.items);
    } else {
      setFilteredItems(list.items.filter(item => item.component_type === type));
    }
  };

  const handleTypeChange = (type) => {
    setActiveType(type);
  };

  const handleViewModeChange = (mode) => {
    setViewMode(mode);
  };

  const handleSortChange = (sort) => {
    setSortBy(sort);

    // Sort filtered items
    let sorted = [...filteredItems];

    switch (sort) {
      case 'name-asc':
        sorted.sort((a, b) => a.display_name.localeCompare(b.display_name));
        break;
      case 'name-desc':
        sorted.sort((a, b) => b.display_name.localeCompare(a.display_name));
        break;
      case 'newest':
        sorted.sort((a, b) => new Date(b.added_at) - new Date(a.added_at));
        break;
      case 'oldest':
        sorted.sort((a, b) => new Date(a.added_at) - new Date(b.added_at));
        break;
      default:
        break;
    }

    setFilteredItems(sorted);
  };

  const handleRemoveItem = async (item) => {
    try {
      await listsApi.removeComponentFromList(
        id,
        item.component_type,
        item.component_id
      );

      // Update the local state by removing the item
      setFilteredItems(prev => prev.filter(i =>
        !(i.component_type === item.component_type && i.component_id === item.component_id)
      ));

      // If list state is available, update it too
      if (list && list.items) {
        setList({
          ...list,
          items: list.items.filter(i =>
            !(i.component_type === item.component_type && i.component_id === item.component_id)
          ),
          parts_count: list.parts_count > 0 ? list.parts_count - 1 : 0
        });
      }

      // Show success message (optional)
      console.log('Item removed successfully');
    } catch (err) {
      console.error('Error removing item:', err);
      // Could add toast notification here
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!list) return <ErrorMessage message="List not found" />;

  return (
    <div className="w-[90%] max-w-6xl mx-auto px-4 py-8">
      {/* Back button */}
      <div className="mb-6 flex justify-between items-center">
        <div>
          <a
            href={ROUTES.PROFILE.CURRENT}
            className="inline-flex items-center text-primary hover:text-gray-600"
          >
            <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
            Back to Lists
          </a>
        </div>

        <button
          className="px-4 py-2 border border-primary text-primary rounded-md hover:bg-gray-50 transition-colors flex items-center gap-2"
          onClick={() => {/* Edit list functionality */}}
        >
          <FontAwesomeIcon icon={faEdit} />
          Edit List
        </button>
      </div>

      {/* List header */}
      <ListDetailHeader
        list={list}
        onRefresh={fetchListData}
      />

      {/* Filter and controls */}
      <ComponentTypeFilter
        activeType={activeType}
        onTypeChange={handleTypeChange}
        viewMode={viewMode}
        onViewModeChange={handleViewModeChange}
        sortBy={sortBy}
        onSortChange={handleSortChange}
        totalCount={filteredItems.length}
        typeCounts={list.parts_count_by_type || {}}
      />

      {/* Component grid */}
      <ListItemGrid
        items={filteredItems}
        viewMode={viewMode}
        onRemoveItem={handleRemoveItem}
        emptyState={{
          title: "No components in this list yet",
          message: "Browse components and add them to your list to see them here."
        }}
      />
    </div>
  );
};

export default ListDetailPage;