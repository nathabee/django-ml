import React, { useEffect,useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import CompetenceHeader from '@app/CompetenceHeader';
import AppRoutes from '@app/router';

// Redirect if at root
//if (window.location.pathname === '/') {
//  window.history.replaceState({}, '', '/competence_dashboard');
//}

const App = () => {
  useEffect(() => {
    // Avoid duplicate script loading
    if (!document.getElementById('google-translate-script')) {
      const script = document.createElement('script');
      script.id = 'google-translate-script';
      script.type = 'text/javascript';
      script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
      document.body.appendChild(script);

      // Define the callback function
      window.googleTranslateElementInit = () => {
        new google.translate.TranslateElement(
          {
            pageLanguage: 'en',
            includedLanguages: 'fr,en',
            autoDisplay: false,
            default: 'fr'
          },
          'google_translate_element'
        );

        // Force default translation after a delay
        //setTimeout(() => {
        //  setDefaultLanguage('French');
        //}, 1000);
      };

    }
  }, []);
 




  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  }, []);

  return (
    <div className="competence-app-container">
      <BrowserRouter basename={window.competenceSettings?.basename || '/'}>
        <div className="translate-box" style={{ padding: '10px', textAlign: 'right' }}>
          🌐 Translate: <span id="google_translate_element"></span>
        </div>

        <div className="app-layout">
          {/* Sidebar */}
          <div className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
            <button
              className="hamburger-icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              ☰
            </button>
            <CompetenceHeader />
          </div>

          {/* Main Content */}
          <div className="content-container">
            <AppRoutes />
          </div>
        </div>
      </BrowserRouter>
    </div>
  );
};

export default App;








/*
// src/app/App.tsx
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import CompetenceHeader from '@app/CompetenceHeader';
import AppRoutes from '@app/router';


// Redirect to /competence_home if current URL is exactly '/'
if (window.location.pathname === '/') {
  window.history.replaceState({}, '', '/competence_home');
}


const App = () => (
  <BrowserRouter basename={window.competenceSettings?.basename || '/'}>
    <CompetenceHeader />
    <AppRoutes />
  </BrowserRouter>
);

export default App;
*/