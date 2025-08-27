// src/hooks/useLogin.ts
'use client';

import { useState } from 'react';
import axios, { AxiosError } from 'axios';
import { useAuth } from '@context/AuthContext';
import useBootstrapData from '@hooks/useBootstrapData';
import { getApiUrl } from '@utils/helper';

export function useLoginHandler() {
  const { login } = useAuth();
  const { fetchBootstrapData } = useBootstrapData();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const apiUrl = getApiUrl().replace(/\/+$/, ''); // ensure no trailing slash

  const handleLogin = async (username: string, password: string, onSuccess: () => void) => {
    try {
      const response = await axios.post(`${apiUrl}/auth/login/`, { username, password });
      const { access: token } = response.data;

      const userResponse = await axios.get(`${apiUrl}/me/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      const userInfo = userResponse.data;
      login(token, userInfo);

      // 🔽 hydrate all frontend data now
      await fetchBootstrapData();

      onSuccess();
    } catch (error) {
      const axiosError = error as AxiosError;
      setErrorMessage(
        axiosError.response?.status === 401 ? 'Invalid username or password' : 'Connection error'
      );
      console.error('Login failed:', error);
    }
  };

  return { handleLogin, errorMessage };
}
