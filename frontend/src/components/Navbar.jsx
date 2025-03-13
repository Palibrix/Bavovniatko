import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <div>
        <Link to="/">Drone Components</Link>
      </div>
      <ul>
        <li><Link to="/components/antennas">Antennas</Link></li>
        <li><Link to="/components/cameras">Cameras</Link></li>
        <li><Link to="/components/frames">Frames</Link></li>
        <li><Link to="/components/motors">Motors</Link></li>
        <li><Link to="/components/propellers">Propellers</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;