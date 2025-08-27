// src/hooks/useBootstrapData.ts
'use client';

import { useAuth } from '@context/AuthContext';
import { api, authHeaders } from '@utils/api';
import { FarmWithFields } from '@mytypes/farm';

type BootstrapOpts = {
  force?: boolean; // bypass cache (optional)
};

export default function useBootstrapData() {
  const { token, farms, setFarms, setActiveFarm } = useAuth();

  const fetchBootstrapData = async (opts: BootstrapOpts = {}) => {
    if (!token) return;
    if (!opts.force && farms.length > 0) return; // already hydrated

    // Add more datasets here later if needed (rows, images, etc.)
    const [farmsRes] = await Promise.all([
      api.get<FarmWithFields[]>('/farms', { headers: authHeaders(token) }),
    ]);

    const farmsData = farmsRes.data || [];
    setFarms(farmsData);

    // Auto-select single farm
    if (farmsData.length === 1) {
      setActiveFarm(farmsData[0]);
    }
  };

  return { fetchBootstrapData };
}
