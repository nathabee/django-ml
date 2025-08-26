'use client';

import { useState, useCallback } from 'react';
import { ShortReport } from '@mytypes/shortreport';
import { getToken, isTokenExpired } from '@utils/jwt';
import { getApiUrl } from '@utils/helper';
import axios from 'axios';
import { useAuth } from '@context/AuthContext';

interface UseShortReportsResult {
  reports: ShortReport[];
  loading: boolean;
  error: boolean;
  fetchReports: () => void;
}

const useShortReports = (): UseShortReportsResult => {
  const [reports, setReports] = useState<ShortReport[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const { logout } = useAuth();

  const fetchReports = useCallback(async () => {
    const token = getToken();

    if (!token || isTokenExpired(token)) {
      logout();
      return;
    }

    setLoading(true);
    setError(false);

    try {
      const apiUrl = getApiUrl();
      const response = await axios.get(`${apiUrl}/shortreports/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setReports(response.data);
    } catch (err) {
      console.error('Error fetching short reports:', err);
      setError(true);
    } finally {
      setLoading(false);
    }
  }, [logout]);

  return {
    reports,
    loading,
    error,
    fetchReports,
  };
};

export default useShortReports;
