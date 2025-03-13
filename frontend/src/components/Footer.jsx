import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer>
      <div className="container">
        <div className="footer-content">
          <div className="copyright">
            &copy; {new Date().getFullYear()} Bavovniantko. All rights reserved.
          </div>
          <div className="footer-links">
            <ul>
              <li><Link to="#">About Us</Link></li>
              <li><Link to="#">Contact</Link></li>
              <li><Link to="#">Privacy Policy</Link></li>
              <li><Link to="#">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;