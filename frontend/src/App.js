import React from 'react';
import { BrowserRouter as Router, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import { getRoutes } from './routes';
import './App.css';

function App() {
  // Get route components from our configuration
  const routeComponents = getRoutes();

  return (
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
)
  ;
}

export default App;