// src/app/router.tsx
 

import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import CompetenceHome from '@pages/CompetenceHome';
import CompetenceLogin from '@pages/CompetenceLogin';
import CompetenceDashboard from '@pages/CompetenceDashboard';
import CompetenceError from '@pages/CompetenceError';
import CompetenceStudentMgt from  '@pages/CompetenceStudentMgt';
import CompetencePdfConf from  '@pages/CompetencePdfConf'; 
import CompetenceCatalogueMgt from  '@pages/CompetenceCatalogueMgt';
import CompetenceReportMgt from  '@pages/CompetenceReportMgt';
import CompetenceOverviewTest from  '@pages/CompetenceOverviewTest';
import CompetencePdfView from  '@pages/CompetencePdfView';

const AppRoutes = () => (
  <Routes>
    
    <Route path="/competence_home" element={<CompetenceHome />} />
    <Route path="/competence_login" element={<CompetenceLogin />} />
    <Route path="/competence_dashboard" element={<CompetenceDashboard />} />
    <Route path="/competence_student_mgt" element={<CompetenceStudentMgt />} />
    <Route path="/competence_pdf_conf" element={<CompetencePdfConf />} />
    <Route path="/competence_catalogue_mgt" element={<CompetenceCatalogueMgt />} />
    <Route path="/competence_report_mgt" element={<CompetenceReportMgt />} />
    <Route path="/competence_overview_test" element={<CompetenceOverviewTest />} /> 
    <Route path="/competence_pdf_view" element={<CompetencePdfView />} />
    <Route path="/competence_error" element={<CompetenceError />} />

    <Route path="/"  element={<CompetenceDashboard />} />
  </Routes>
);

export default AppRoutes;
 
  