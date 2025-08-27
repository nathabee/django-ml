// src/components/UserDisplay.tsx
'use client';
import React from 'react';
import { useAuth } from '@context/AuthContext';

const UserDisplay: React.FC = () => {
  const { user } = useAuth();
  return (
    <div className="mb-3">
      {user ? <span>Welcome, <strong>{user.first_name} {user.last_name}</strong></span> : null}
    </div>
  );
};

export default UserDisplay;
