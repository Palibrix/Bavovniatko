import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark-bg py-8">
      <div className="w-[90%] max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-6 md:mb-0 text-light-text">
            &copy; {currentYear} Bavovniantko. All rights reserved.
          </div>

          <nav className="flex flex-wrap justify-center">
            <Link to="#" className="text-light-text hover:text-secondary transition-colors mx-4 my-2">
              Contact
            </Link>
            <Link to="#" className="text-light-text hover:text-secondary transition-colors mx-4 my-2">
              Privacy Policy
            </Link>
            <Link to="#" className="text-light-text hover:text-secondary transition-colors mx-4 my-2">
              Terms of Service
            </Link>
          </nav>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-700 text-center text-gray-400 text-sm">
          <p>Bavovniantko Drone Builder — Find the perfect components for your custom build</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;