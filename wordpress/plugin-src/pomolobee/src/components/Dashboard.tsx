// src/components/Dashboard.tsx
'use client';

import React from "react";
import { useProtectedPage } from "@hooks/useProtectedPage";
import FieldSelection from "@components/FieldSelection";
import ActiveContextCard from "@components/ActiveContextCard";

const Dashboard: React.FC = () => {
  useProtectedPage(); // redirects if not logged

  return (
    <>
      <h1>📊 Dashboard</h1>
      <FieldSelection />
      <ActiveContextCard />
    </>
  );
};

export default Dashboard;
