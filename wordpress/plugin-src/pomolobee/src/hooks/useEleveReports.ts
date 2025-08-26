// src/hooks/useEleveReports.ts
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Report } from '@mytypes/report';
import { Eleve } from '@mytypes/eleve';
import { getToken } from '@utils/jwt';
import { getApiUrl } from '@utils/helper';

export const useEleveReports = (eleve: Eleve) => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const token = getToken();
        const res = await axios.get(`${getApiUrl()}/eleve/${eleve.id}/reports/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setReports(res.data);
      } catch (err) {
        console.error('Error fetching reports:', err);
        setError('Failed to fetch reports');
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [eleve]);

  return { reports, loading, error };
};
