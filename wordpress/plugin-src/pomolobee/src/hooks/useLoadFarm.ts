// src/hooks/useLoadFarms.ts
'use client';
import { useEffect } from 'react';
import { useAuth } from '@context/AuthContext';
import { api, authHeaders } from '@utils/api';
import { FarmWithFields } from '@mytypes/farm';

export function useLoadFarms() {
  const { token, farms, setFarms, setActiveFarm } = useAuth();

  useEffect(() => {
    if (!token) return;
    if (farms.length > 0) return; // already loaded

    (async () => {
      // Adjust to your real endpoint
      const r = await api.get<FarmWithFields[]>('/farms/', {
        headers: authHeaders(token),
      });
      const data = r.data || [];
      setFarms(data);
      if (data.length === 1) setActiveFarm(data[0]); // auto-select single farm
    })().catch(console.error);
  }, [token, farms.length, setFarms, setActiveFarm]);
}
