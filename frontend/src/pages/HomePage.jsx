import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../routes';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass, faTools, faCog, faFan, faMicrochip, faTachometerAlt,
         faBroadcastTower, faBorderAll, faCamera, faSatelliteDish, faWifi } from '@fortawesome/free-solid-svg-icons';
import ComponentCard from '../components/ComponentCard';

function HomePage() {
  return (
    <>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-[#3a6ea5] to-[#7c98b3] text-white py-24 relative overflow-hidden">
        {/* Pattern overlay */}
        <div className="absolute top-0 left-0 w-full h-full opacity-50"
             style={{
               backgroundImage: `
                 radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 1%, transparent 1.5%),
                 radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.1) 1%, transparent 1.5%),
                 radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.1) 2%, transparent 2.5%)
               `,
               backgroundSize: '6rem 6rem',
               backgroundPosition: '0 0, 3rem 3rem, 1.5rem 1.5rem'
             }}>
        </div>

        <div className="w-[90%] max-w-6xl mx-auto px-4">
          <div className="flex flex-col items-center justify-center text-center relative max-w-3xl mx-auto">
            <div>
              <h1 className="text-6xl font-bold mb-6 leading-tight">Build Your Perfect Drone</h1>
              <p className="text-xl text-white/90 mb-10 max-w-2xl">
                Customize every aspect of your drone with our extensive catalog of components.
                Select individual parts or explore complete builds to create your ideal flying machine.
              </p>
            </div>
            <div className="flex gap-6 justify-center flex-wrap">
              <Link to={ROUTES.BUILDS.DRONES.LIST} className="inline-flex items-center py-3 px-8 rounded-lg font-semibold transition-all duration-300 text-lg bg-light-bg text-primary hover:bg-white hover:translate-y-[-2px] hover:shadow-lg">
                <i className="mr-3 text-xl">
                  <FontAwesomeIcon icon={faMagnifyingGlass} />
                </i>
                Explore Drones
              </Link>
              <Link to={ROUTES.BUILDS.DRONES.CREATE} className="inline-flex items-center py-3 px-8 rounded-lg font-semibold transition-all duration-300 text-lg bg-transparent text-white border-2 border-white hover:bg-white/10 hover:translate-y-[-2px]">
                <i className="mr-3 text-xl">
                  <FontAwesomeIcon icon={faTools} />
                </i>
                Create Your Own
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Components Section */}
      <section className="py-16">
        <div className="w-[90%] max-w-6xl mx-auto px-4">
          <h2 className="text-center mb-3 text-4xl font-bold text-primary">Drone Components</h2>
          <p className="text-center max-w-2xl mx-auto mb-12 text-gray-500 text-lg">
            Choose from our extensive catalog of drone components to start your custom build.
            Each component category includes detailed specifications and compatibility information.
          </p>

          {/* Propulsion Components */}
          <div className="mb-12">
            <h3 className="text-2xl mb-6 pb-2 border-b border-gray-200 font-semibold text-primary">Propulsion Components</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <ComponentCard
                title="Motors"
                icon={faCog}
                heading="Drone Motors"
                description="Browse electric motors that power your drone's flight with various KV ratings, sizes, and power outputs."
                colorType="propulsion"
                to={ROUTES.COMPONENTS.MOTORS.LIST}
              />

              <ComponentCard
                title="Propellers"
                icon={faFan}
                heading="Drone Propellers"
                description="Explore propellers of different sizes, pitches, and blade counts to optimize your drone's performance."
                colorType="propulsion"
                to={ROUTES.COMPONENTS.PROPELLERS.LIST}
              />
            </div>
          </div>

          {/* Control Systems */}
          <div className="mb-12">
            <h3 className="text-2xl mb-6 pb-2 border-b border-gray-200 font-semibold text-primary">Control Systems</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <ComponentCard
                title="Flight Controllers"
                icon={faMicrochip}
                heading="Flight Control Units"
                description="The brain of your drone that processes inputs and controls flight dynamics."
                colorType="control"
                to={ROUTES.COMPONENTS.FLIGHT_CONTROLLERS.LIST}
              />

              <ComponentCard
                title="Speed Controllers"
                icon={faTachometerAlt}
                heading="Electronic Speed Controllers"
                description="Regulate motor speed with precision for optimal flight control."
                colorType="control"
                to={ROUTES.COMPONENTS.SPEED_CONTROLLERS.LIST}
              />

              <ComponentCard
                title="Receivers"
                icon={faBroadcastTower}
                heading="Radio Receivers"
                description="Receive control signals from your transmitter to operate the drone."
                colorType="control"
                to={ROUTES.COMPONENTS.RECEIVERS.LIST}
              />
            </div>
          </div>

          {/* Structure & Communications */}
          <div className="mb-12">
            <h3 className="text-2xl mb-6 pb-2 border-b border-gray-200 font-semibold text-primary">Structure & Communications</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <ComponentCard
                title="Frames"
                icon={faBorderAll}
                heading="Drone Frames"
                description="Structural foundation that holds all components together in various configurations."
                colorType="frame"
                to={ROUTES.COMPONENTS.FRAMES.LIST}
              />

              <ComponentCard
                title="Cameras"
                icon={faCamera}
                heading="FPV & Recording Cameras"
                description="Capture stunning aerial footage with specialized drone cameras."
                colorType="video"
                to={ROUTES.COMPONENTS.CAMERAS.LIST}
              />

              <ComponentCard
                title="Transmitters"
                icon={faSatelliteDish}
                heading="Video Transmitters"
                description="Broadcast real-time video feed from your drone to your display or goggles."
                colorType="video"
                to={ROUTES.COMPONENTS.TRANSMITTERS.LIST}
              />

              <ComponentCard
                title="Antennas"
                icon={faWifi}
                heading="Transmitter & Receiver Antennas"
                description="Improve signal quality and range with specialized antennas."
                colorType="antenna"
                to={ROUTES.COMPONENTS.ANTENNAS.LIST}
              />
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default HomePage;