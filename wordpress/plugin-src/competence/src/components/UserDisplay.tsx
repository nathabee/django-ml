'use client';

import React from 'react';
import { User } from '@mytypes/user'; // Use your actual alias for types

interface UserDisplayProps {
  user?: User | null;
}

const UserDisplay: React.FC<UserDisplayProps> = ({ user }) => {
  if (!user) {
    return <p>No user data available.</p>;
  }

  return (
    <div>
      {user.first_name} {user.last_name} — ID: {user.username}, Language: {user.lang}, Roles: {user.roles.join(', ')}
    </div>
  );
};

export default UserDisplay;
