// src/app/PomoloBeeHeader.tsx
import React from 'react';
import { useAuth } from '@context/AuthContext';
import { Link } from 'react-router-dom';



const PomoloBeeHeader = () => {
  const { isLoggedIn, logout, activeEleve, activeCatalogues, activeLayout, user } = useAuth();

  const canAccessReport = activeEleve && activeCatalogues.length && activeLayout && user;


  return (
    <nav className="navbar sticky-navbar">
      <div className="navbar-container">
        <div className="navbar-active-data">
          <Link to="/pomolobee_home" className="nav-link">🏠 Home</Link>

          {isLoggedIn ? (
            <>
              <Link to="/pomolobee_dashboard" className="nav-link">📊 Dashboard</Link>
              <Link to="/pomolobee_student_mgt" className="nav-link">👨‍🎓 Student Management</Link>
              <Link to="/pomolobee_pdf_conf" className="nav-link">🛠️ PDF Setup</Link>
              <Link to="/pomolobee_catalogue_mgt" className="nav-link">📚 Catalogue Management</Link>
              {canAccessReport ? (
                <>
                  <Link to="/pomolobee_report_mgt" className="nav-link">📄 Report Management</Link>
                  <Link to="/pomolobee_overview_test" className="nav-link">🧪 Ongoing Tests</Link>
                  <Link to="/pomolobee_pdf_view" className="nav-link">🖨️ PDF Viewer</Link>
                </>
              ) : (
                <>
                  <span className="nav-link disabled">📄 Report Management</span>
                  <span className="nav-link disabled">🧪 Ongoing Tests</span>
                  <span className="nav-link disabled">🖨️ PDF Viewer</span>
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

