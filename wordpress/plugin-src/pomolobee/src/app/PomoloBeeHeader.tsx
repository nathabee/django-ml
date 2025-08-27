// src/app/PomoloBeeHeader.tsx
import React from 'react';
import { useAuth } from '@context/AuthContext';
import { Link } from 'react-router-dom';



const PomoloBeeHeader = () => {
  const { isLoggedIn, logout, activeFarm , user } = useAuth();

  const canAccessFarm = activeFarm && user;


  return (
    <nav className="navbar sticky-navbar">
      <div className="navbar-container">
        <div className="navbar-active-data">
          <Link to="/pomolobee_home" className="nav-link">🏠 Home</Link>

          {isLoggedIn ? (
            <>
              <Link to="/pomolobee_dashboard" className="nav-link">📊 Dashboard</Link>
              {canAccessFarm ? (
                <>
                  <Link to="/pomolobee_Farm" className="nav-link">📄 Farm Management</Link> 
                </>
              ) : (
                <>
                  <span className="nav-link disabled">Please select a farm</span>
                </>
              )}

              <button className="navbar-button" onClick={logout}>🔓 Logout</button>
            </>
          ) : (
            <Link to="/pomolobee_login" className="nav-link">🔓 Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default PomoloBeeHeader;

