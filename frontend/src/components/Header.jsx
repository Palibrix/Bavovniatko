import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../routes';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane, faCog, faFan, faMicrochip, faTachometerAlt, faBroadcastTower,
         faBorderAll, faCamera, faSatelliteDish, faWifi, faChevronDown } from '@fortawesome/free-solid-svg-icons';

function Header() {
  // State to manage dropdown visibility
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    }

    // Add event listener if dropdown is open
    if (dropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    // Cleanup
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownOpen]);

  // Toggle dropdown
  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  return (
    <header className="bg-dark-bg text-light-text py-5 shadow-md relative z-10">
      <div className="w-[90%] max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center">
          <Link to={ROUTES.HOME} className="text-2xl font-bold text-light-text no-underline flex items-center">
            <i className="mr-2 text-secondary">
              <FontAwesomeIcon icon={faPaperPlane} />
            </i>
            Bavovniantko
          </Link>
          <nav>
            <ul className="flex list-none gap-6">
              <li><Link to={ROUTES.HOME} className="text-light-text no-underline font-medium transition-colors hover:text-secondary flex items-center">Home</Link></li>
              <li className="relative" ref={dropdownRef}>
                <button
                  onClick={toggleDropdown}
                  className="text-light-text no-underline font-medium transition-colors hover:text-secondary flex items-center bg-transparent border-none cursor-pointer"
                >
                  Components
                  <span className="ml-2 transition-transform duration-300" style={{ transform: dropdownOpen ? 'rotate(180deg)' : 'rotate(0)' }}>
                    <FontAwesomeIcon icon={faChevronDown} size="xs" />
                  </span>
                </button>
                {dropdownOpen && (
                  <div
                    className="absolute top-full left-0 w-[300px] bg-white rounded-lg shadow-xl p-4 flex flex-col z-50 mt-2"
                    onClick={(e) => e.stopPropagation()} // Prevent clicks inside dropdown from closing it
                  >
                    {/* Propulsion Components */}
                    <div className="mb-3">
                      <h3 className="text-sm text-gray-500 uppercase mb-2 pb-1 border-b border-gray-100">Propulsion</h3>
                      <div className="grid grid-cols-2 gap-2">
                        <Link
                          to='#'
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-propulsion-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faCog} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Motors</span>
                        </Link>
                        <Link
                          to="#"
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-propulsion-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faFan} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Propellers</span>
                        </Link>
                      </div>
                    </div>

                    {/* Control Systems */}
                    <div className="mb-3">
                      <h3 className="text-sm text-gray-500 uppercase mb-2 pb-1 border-b border-gray-100">Control Systems</h3>
                      <div className="grid grid-cols-2 gap-2">
                        <Link
                          to="#"
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-control-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faMicrochip} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Flight Controllers</span>
                        </Link>
                        <Link
                          to="#"
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-control-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faTachometerAlt} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Speed Controllers</span>
                        </Link>
                        <Link
                          to="#"
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-control-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faBroadcastTower} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Receivers</span>
                        </Link>
                      </div>
                    </div>

                    {/* Structure & Communications */}
                    <div className="mb-3">
                      <h3 className="text-sm text-gray-500 uppercase mb-2 pb-1 border-b border-gray-100">Structure & Communications</h3>
                      <div className="grid grid-cols-2 gap-2">
                        <Link
                          to="#"
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-frame-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faBorderAll} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Frames</span>
                        </Link>
                        <Link
                          to='#'
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-video-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faCamera} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Cameras</span>
                        </Link>
                        <Link
                          to="#"
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-video-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faSatelliteDish} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Transmitters</span>
                        </Link>
                        <Link
                          to={ROUTES.COMPONENTS.ANTENNAS.LIST}
                          className="flex items-center text-text-color p-2 rounded-md transition-colors hover:bg-gray-50"
                        >
                          <div className="w-7 h-7 rounded-full flex justify-center items-center mr-2 flex-shrink-0 bg-antenna-color">
                            <i className="text-sm text-white">
                              <FontAwesomeIcon icon={faWifi} />
                            </i>
                          </div>
                          <span className="text-sm font-medium">Antennas</span>
                        </Link>
                      </div>
                    </div>
                  </div>
                )}
              </li>
              <li><Link to="#" className="text-light-text no-underline font-medium transition-colors hover:text-secondary flex items-center">Builds</Link></li>
              <li><Link to="#" className="text-light-text no-underline font-medium transition-colors hover:text-secondary flex items-center">Suggest Component</Link></li>
              <li><Link to="#" className="text-light-text no-underline font-medium transition-colors hover:text-secondary flex items-center">Login</Link></li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;