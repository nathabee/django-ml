// src/hooks/useLogin.ts
'use client';

import { useState } from 'react';
import axios, { AxiosError } from 'axios';
import { useAuth } from '@context/AuthContext';
import useBootstrapData from '@hooks/useBootstrapData';
import { apiUser, authHeaders } from '@utils/api';


export function useLoginHandler() {
  const { login } = useAuth();
  const { fetchBootstrapData } = useBootstrapData();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
 

  const handleLogin = async (username: string, password: string, onSuccess: () => void) => {
    try { 


      const response = await apiUser.post("/auth/login/",  { username, password });

      const { access: token } = response.data;

 

      const userResponse = await apiUser.get("/me/", { headers: authHeaders(token) });


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
