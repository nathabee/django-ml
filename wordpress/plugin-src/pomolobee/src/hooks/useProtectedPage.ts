// src/hooks/useProtectedPage.ts
'use client';
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { getToken, isTokenExpired } from '@utils/jwt';

export const useProtectedPage = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();

  useEffect(() => {
    const token = getToken();
    const needsAuth = !token || isTokenExpired(token);
    const isOnLogin = pathname.includes('pomolobee_login');

    if (needsAuth && !isOnLogin) {
      navigate('/pomolobee_login');
    }
  }, [navigate, pathname]);
};
