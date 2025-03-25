import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../routes';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import ComponentsDropdown from './header/ComponentsDropdown';
import UserDropdown from './header/UserDropdown';
import { useAuth } from '../context/AuthContext';

function Header() {
  const { isAuthenticated } = useAuth();

  return (
    <header className="bg-dark-bg text-light-text py-5 shadow-md relative z-10">
      <div className="w-[90%] max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center">
          {/* Logo and brand name */}
          <Link to={ROUTES.HOME} className="text-2xl font-bold text-light-text no-underline flex items-center">
            <FontAwesomeIcon icon={faPaperPlane} className="mr-2 text-secondary" />
            Bavovniantko
          </Link>

          {/* Navigation */}
          <nav>
            <ul className="flex list-none gap-6">
              <li>
                <Link to={ROUTES.HOME} className="text-light-text no-underline font-medium hover:text-secondary transition-colors">
                  Home
                </Link>
              </li>

              {/* Components dropdown */}
              <li className="relative">
                <ComponentsDropdown />
              </li>

              <li>
                <Link to={ROUTES.BUILDS.DRONES.LIST} className="text-light-text no-underline font-medium hover:text-secondary transition-colors">
                  Builds
                </Link>
              </li>

              <li>
                <Link to="#" className="text-light-text no-underline font-medium hover:text-secondary transition-colors">
                  Suggest Component
                </Link>
              </li>

              {/* Conditional rendering based on authentication state */}
              {isAuthenticated ? (
                <li className="relative">
                  <UserDropdown />
                </li>
              ) : (
                <li>
                  <Link
                    to={ROUTES.AUTH}
                    className="text-light-text no-underline font-medium hover:text-secondary transition-colors"
                  >
                    Login
                  </Link>
                </li>
              )}
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;