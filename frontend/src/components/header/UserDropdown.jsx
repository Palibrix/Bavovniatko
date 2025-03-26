import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faSignOutAlt, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../../context/AuthContext';
import Dropdown, { DropdownSection, DropdownItem } from '../common/Dropdown';
import {ROUTES} from "../../routes";

/**
 * User dropdown menu in header
 */
const UserDropdown = () => {
  const { user, logout } = useAuth();

  // Handle logout
  const handleLogout = async () => {
    await logout();
  };

  // Custom trigger for the dropdown
  const dropdownTrigger = (
    <button className="text-light-text hover:text-secondary transition-colors flex items-center">
      {user?.username || 'User'}
      <FontAwesomeIcon
        icon={faChevronDown}
        className="ml-2 text-xs"
      />
    </button>
  );

  return (
    <Dropdown trigger={dropdownTrigger} width="sm">
      <DropdownSection>
        <DropdownItem
          icon={<FontAwesomeIcon icon={faUser} />}
          href={ROUTES.PROFILE.CURRENT}
        >
          Profile
        </DropdownItem>

        <DropdownItem
          icon={<FontAwesomeIcon icon={faSignOutAlt} />}
          onClick={handleLogout}
        >
          Logout
        </DropdownItem>
      </DropdownSection>
    </Dropdown>
  );
};

export default UserDropdown;