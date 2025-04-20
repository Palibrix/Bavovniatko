import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faSync } from '@fortawesome/free-solid-svg-icons';
import { listsApi } from '../../services/api';
import ListDetailHeader from '../../components/lists/ListDetailHeader';
import ComponentTypeFilter from '../../components/lists/ComponentTypeFilter';
import ListItemGrid from '../../components/lists/ListItemGrid';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import ErrorMessage from '../../components/common/ErrorMessage';
import Toast from '../../components/common/Toast';
import ConfirmationModal from '../../components/common/ConfirmationModal';
import CreateListModal from '../../components/lists/CreateListModal';
import { ROUTES } from '../../routes';

const ListDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // List state
  const [list, setList] = useState(null);
  const [listItems, setListItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  // UI state
  const [activeType, setActiveType] = useState('all');
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'grid'
  const [sortBy, setSortBy] = useState('name-asc');
  const [toast, setToast] = useState({ visible: false, message: '', type: '' });

  // Edit and delete state
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // Fetch list data
  useEffect(() => {
    fetchListData();
  }, [id]);

  // Fetch list data whenever active type changes
  useEffect(() => {
    if (list) {
      if (activeType === 'all') {
        // All items are already in the list data
        setListItems(list.items || []);
      } else {
        // Fetch specific component type
        fetchItemsByType(activeType);
      }
    }
  }, [activeType, list]);

  const fetchListData = async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await listsApi.getListById(id);
      setList(data);
      setListItems(data.items || []);

      setLoading(false);
    } catch (err) {
      console.error('Error fetching list:', err);
      setError(err.message || 'Failed to load list details');
      setLoading(false);
    }
  };

  const fetchItemsByType = async (type) => {
    try {
      const items = await listsApi.getListItemsByType(id, type);
      setListItems(items);
    } catch (err) {
      console.error(`Error fetching ${type} items:`, err);
      // Show toast error but don't set main error state
      setToast({
        visible: true,
        message: `Failed to load ${type} items`,
        type: 'error'
      });
    }
  };

  const handleRefreshList = async () => {
    setRefreshing(true);

    try {
      await fetchListData();
      setToast({
        visible: true,
        message: 'List refreshed successfully',
        type: 'success'
      });
    } catch (err) {
      // Error is already set in fetchListData
    } finally {
      setRefreshing(false);
    }
  };

  // Edit list handlers
  const handleEditList = () => {
    setShowEditModal(true);
  };

  const handleEditSuccess = (updatedList) => {
    // Update list in state
    setList(prev => ({
      ...prev,
      ...updatedList
    }));

    setToast({
      visible: true,
      message: 'List updated successfully',
      type: 'success'
    });
  };

  // Delete list handlers
  const handleDeleteList = () => {
    setShowDeleteConfirm(true);
  };

  const confirmDeleteList = async () => {
    try {
      setDeleting(true);

      // Call API to delete list
      await listsApi.deleteList(id);

      // Show success toast
      setToast({
        visible: true,
        message: 'List deleted successfully',
        type: 'success'
      });

      // Navigate back to lists
      navigate(ROUTES.PROFILE.CURRENT);
    } catch (err) {
      console.error('Error deleting list:', err);
      setToast({
        visible: true,
        message: 'Failed to delete list',
        type: 'error'
      });
      setDeleting(false);
    }
  };

  const handleRemoveComponent = async (item) => {
    try {
      // Call API to remove component
      await listsApi.removeComponentFromList(
        id,
        item.component_type,
        item.component_id
      );

      // Update total count in list
      if (list && list.parts_count) {
        setList(prev => ({
          ...prev,
          parts_count: prev.parts_count - 1
        }));
      }

      // Refetch the list items based on current filter
      if (activeType === 'all') {
        // Refetch all list data to get fresh items
        await fetchListData();
      } else {
        // Only refetch the filtered items
        await fetchItemsByType(activeType);
      }

      setToast({
        visible: true,
        message: 'Component removed from list',
        type: 'success'
      });
    } catch (err) {
      console.error('Error removing component:', err);
      setToast({
        visible: true,
        message: 'Failed to remove component',
        type: 'error'
      });
    }
  };

  // Get component type counts for filtering
  const getComponentCounts = () => {
    if (!list || !list.parts_count_by_type) {
      return {};
    }

    return list.parts_count_by_type;
  };

  if (loading && !list) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchListData} />;
  }

  if (!list) {
    return <ErrorMessage message="List not found" />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Back button */}
      <Link
        to={ROUTES.PROFILE.CURRENT}
        className="inline-flex items-center text-primary hover:text-gray-600 mb-6"
      >
        <FontAwesomeIcon icon={faArrowLeft} className="mr-2" />
        Back to Profile
      </Link>

      {/* List header with actions */}
      <ListDetailHeader
        list={list}
        onRefresh={handleRefreshList}
        onEdit={handleEditList}
      />

      {/* Component filtering */}
      <ComponentTypeFilter
        activeType={activeType}
        onTypeChange={setActiveType}
        viewMode={viewMode}
        onViewModeChange={setViewMode}
        sortBy={sortBy}
        onSortChange={setSortBy}
        totalCount={list.parts_count || 0}
        typeCounts={getComponentCounts()}
      />

      {/* Component list */}
      <ListItemGrid
        items={listItems}
        viewMode={viewMode}
        onRemoveItem={handleRemoveComponent}
        emptyState={{
          title: activeType === 'all'
            ? "No components in this list"
            : `No ${activeType} components in this list`,
          message: "Add components to your list by browsing components and clicking 'Add to List'"
        }}
      />

      {/* Edit list modal */}
      <CreateListModal
        isOpen={showEditModal}
        onClose={() => setShowEditModal(false)}
        onSuccess={handleEditSuccess}
        list={list}
        onDelete={handleDeleteList}
      />

      {/* Delete confirmation modal */}
      <ConfirmationModal
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        onConfirm={confirmDeleteList}
        title="Delete List"
        message={`Are you sure you want to delete the list "${list.name}"? This action cannot be undone.`}
        confirmText={deleting ? "Deleting..." : "Delete"}
        cancelText="Cancel"
        type="danger"
      />

      {/* Toast notifications */}
      {toast.visible && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({...toast, visible: false})}
        />
      )}
    </div>
  );
};

export default ListDetailPage;