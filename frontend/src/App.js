import React from 'react';
import { BrowserRouter as Router, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import { getRoutes } from './routes';
import { AuthProvider } from './context/AuthContext';
import './App.css';

function App() {
  // Get route components from our configuration
  const routeComponents = getRoutes();

  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Header/>
          <div className="content">
            <Routes>
              {routeComponents}
            </Routes>
          </div>
          <Footer/>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;