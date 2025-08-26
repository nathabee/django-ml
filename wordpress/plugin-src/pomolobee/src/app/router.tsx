// src/app/router.tsx
 

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import PomoloBeeHome from '@pages/PomoloBeeHome';
import PomoloBeeLogin from '@pages/PomoloBeeLogin';
import PomoloBeeDashboard from '@pages/PomoloBeeDashboard';
import PomoloBeeError from '@pages/PomoloBeeError';
import PomoloBeeStudentMgt from  '@pages/PomoloBeeStudentMgt';
import PomoloBeePdfConf from  '@pages/PomoloBeePdfConf'; 
import PomoloBeeCatalogueMgt from  '@pages/PomoloBeeCatalogueMgt';
import PomoloBeeReportMgt from  '@pages/PomoloBeeReportMgt';
import PomoloBeeOverviewTest from  '@pages/PomoloBeeOverviewTest';
import PomoloBeePdfView from  '@pages/PomoloBeePdfView';

const AppRoutes = () => (
  <Routes>
    
    <Route path="/pomolobee_home" element={<PomoloBeeHome />} />
    <Route path="/pomolobee_login" element={<PomoloBeeLogin />} />
    <Route path="/pomolobee_dashboard" element={<PomoloBeeDashboard />} />
    <Route path="/pomolobee_student_mgt" element={<PomoloBeeStudentMgt />} />
    <Route path="/pomolobee_pdf_conf" element={<PomoloBeePdfConf />} />
    <Route path="/pomolobee_catalogue_mgt" element={<PomoloBeeCatalogueMgt />} />
    <Route path="/pomolobee_report_mgt" element={<PomoloBeeReportMgt />} />
    <Route path="/pomolobee_overview_test" element={<PomoloBeeOverviewTest />} /> 
    <Route path="/pomolobee_pdf_view" element={<PomoloBeePdfView />} />
    <Route path="/pomolobee_error" element={<PomoloBeeError />} />

    <Route path="/"  element={<PomoloBeeDashboard />} />
  </Routes>
);

export default AppRoutes;
 
  