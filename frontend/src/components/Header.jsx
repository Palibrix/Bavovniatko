import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../routes';

function Header() {
  return (
    <header>
      <div className="container">
        <div className="header-content">
          <Link to={ROUTES.HOME} className="logo">
            <i className="fas fa-drone"></i>
            Bavovniantko
          </Link>
          <nav>
            <ul>
              <li><Link to={ROUTES.HOME}>Home</Link></li>
              <li className="dropdown">
                <Link to="#" className="dropdown-toggle">Components</Link>
                <div className="dropdown-menu">
                  {/* Propulsion Components */}
                  <div className="dropdown-category">
                    <h3>Propulsion</h3>
                    <div className="dropdown-items">
                      <Link to='#' className="dropdown-item propulsion-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-cog"></i>
                        </div>
                        <span>Motors</span>
                      </Link>
                      <Link to="#" className="dropdown-item propulsion-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-fan"></i>
                        </div>
                        <span>Propellers</span>
                      </Link>
                    </div>
                  </div>

                  {/* Control Systems */}
                  <div className="dropdown-category">
                    <h3>Control Systems</h3>
                    <div className="dropdown-items">
                      <Link to="#" className="dropdown-item control-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-microchip"></i>
                        </div>
                        <span>Flight Controllers</span>
                      </Link>
                      <Link to="#" className="dropdown-item control-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-tachometer-alt"></i>
                        </div>
                        <span>Speed Controllers</span>
                      </Link>
                      <Link to="#" className="dropdown-item control-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-broadcast-tower"></i>
                        </div>
                        <span>Receivers</span>
                      </Link>
                    </div>
                  </div>

                  {/* Structure & Communications */}
                  <div className="dropdown-category">
                    <h3>Structure & Communications</h3>
                    <div className="dropdown-items">
                      <Link to="#" className="dropdown-item frame-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-border-all"></i>
                        </div>
                        <span>Frames</span>
                      </Link>
                      <Link to='#' className="dropdown-item video-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-camera"></i>
                        </div>
                        <span>Cameras</span>
                      </Link>
                      <Link to="#" className="dropdown-item video-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-satellite-dish"></i>
                        </div>
                        <span>Transmitters</span>
                      </Link>
                      <Link to={ROUTES.COMPONENTS.ANTENNAS.LIST} className="dropdown-item antenna-item">
                        <div className="dropdown-item-icon">
                          <i className="fas fa-wifi"></i>
                        </div>
                        <span>Antennas</span>
                      </Link>
                    </div>
                  </div>
                </div>
              </li>
              <li><Link to="#">Builds</Link></li>
              <li><Link to="#">Suggest Component</Link></li>
              <li><Link to="#">Login</Link></li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;