import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../routes';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass, faTools} from '@fortawesome/free-solid-svg-icons';

function HomePage() {
  return (
    <>
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <div className="hero-text">
              <h1>Build Your Perfect Drone</h1>
              <p>
                Customize every aspect of your drone with our extensive catalog of components.
                Select individual parts or explore complete builds to create your ideal flying machine.
              </p>
            </div>
            <div className="hero-buttons">
              <Link to="#" className="btn btn-primary">
                <i>
                  <FontAwesomeIcon icon={faMagnifyingGlass} />
                </i>
                Explore Drones
              </Link>
              <Link to="#" className="btn btn-secondary">
                <i>
                  <FontAwesomeIcon icon={faTools} />
                </i>
                Create Your Own
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2 className="section-title">Drone Components</h2>
          <p className="section-description">
            Choose from our extensive catalog of drone components to start your custom build.
            Each component category includes detailed specifications and compatibility information.
          </p>

          {/* Propulsion Components */}
          <div className="component-group">
            <h3 className="group-title">Propulsion Components</h3>
            <div className="component-grid">
              {/* Motors Card */}
              <Link to='#' className="component-card propulsion">
                <div className="card-header">Motors</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-cog"></i>
                  </div>
                  <div className="card-content">
                    <h4>Drone Motors</h4>
                    <p>Browse electric motors that power your drone's flight with various KV ratings, sizes, and power outputs.</p>
                  </div>
                </div>
              </Link>

              {/* Propellers Card */}
              <Link to="#" className="component-card propulsion">
                <div className="card-header">Propellers</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-fan"></i>
                  </div>
                  <div className="card-content">
                    <h4>Drone Propellers</h4>
                    <p>Explore propellers of different sizes, pitches, and blade counts to optimize your drone's performance.</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>

          {/* Control Systems */}
          <div className="component-group">
            <h3 className="group-title">Control Systems</h3>
            <div className="component-grid">
              {/* Flight Controllers Card */}
              <Link to="#" className="component-card control">
                <div className="card-header">Flight Controllers</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-microchip"></i>
                  </div>
                  <div className="card-content">
                    <h4>Flight Control Units</h4>
                    <p>The brain of your drone that processes inputs and controls flight dynamics.</p>
                  </div>
                </div>
              </Link>

              {/* Speed Controllers Card */}
              <Link to="#" className="component-card control">
                <div className="card-header">Speed Controllers</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-tachometer-alt"></i>
                  </div>
                  <div className="card-content">
                    <h4>Electronic Speed Controllers</h4>
                    <p>Regulate motor speed with precision for optimal flight control.</p>
                  </div>
                </div>
              </Link>

              {/* Receivers Card */}
              <Link to="#" className="component-card control">
                <div className="card-header">Receivers</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-broadcast-tower"></i>
                  </div>
                  <div className="card-content">
                    <h4>Radio Receivers</h4>
                    <p>Receive control signals from your transmitter to operate the drone.</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>

          {/* Structure & Communications */}
          <div className="component-group">
            <h3 className="group-title">Structure & Communications</h3>
            <div className="component-grid">
              {/* Frames Card */}
              <Link to="#" className="component-card frame">
                <div className="card-header">Frames</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-border-all"></i>
                  </div>
                  <div className="card-content">
                    <h4>Drone Frames</h4>
                    <p>Structural foundation that holds all components together in various configurations.</p>
                  </div>
                </div>
              </Link>

              {/* Cameras Card */}
              <Link to='#' className="component-card video">
                <div className="card-header">Cameras</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-camera"></i>
                  </div>
                  <div className="card-content">
                    <h4>FPV & Recording Cameras</h4>
                    <p>Capture stunning aerial footage with specialized drone cameras.</p>
                  </div>
                </div>
              </Link>

              {/* Transmitters Card */}
              <Link to="#" className="component-card video">
                <div className="card-header">Transmitters</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-satellite-dish"></i>
                  </div>
                  <div className="card-content">
                    <h4>Video Transmitters</h4>
                    <p>Broadcast real-time video feed from your drone to your display or goggles.</p>
                  </div>
                </div>
              </Link>

              {/* Antennas Card */}
              <Link to={ROUTES.COMPONENTS.ANTENNAS.LIST} className="component-card antenna">
                <div className="card-header">Antennas</div>
                <div className="card-body">
                  <div className="card-icon">
                    <i className="fas fa-wifi"></i>
                  </div>
                  <div className="card-content">
                    <h4>Transmitter & Receiver Antennas</h4>
                    <p>Improve signal quality and range with specialized antennas.</p>
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default HomePage;