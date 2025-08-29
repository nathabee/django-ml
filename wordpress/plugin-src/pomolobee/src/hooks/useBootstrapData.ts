// src/hooks/useBootstrapData.ts
'use client';

import { useAuth } from '@context/AuthContext';
import { apiPom, authHeaders } from '@utils/api';
import { FarmWithFields } from '@mytypes/farm';
import { Field } from '@mytypes/field';
import { Fruit } from '@mytypes/fruit';

type BootstrapOpts = { force?: boolean };

export default function useBootstrapData() {
  const {
    token,
    farms, setFarms,
    fields, setFields,
    fruits, setFruits,
    setActiveFarm,
  } = useAuth();

  const fetchBootstrapData = async (opts: BootstrapOpts = {}) => {
    if (!token) return;

    const needFarms  = opts.force || farms.length  === 0;
    const needFields = opts.force || fields.length === 0;
    const needFruits = opts.force || fruits.length === 0;
    if (!needFarms && !needFields && !needFruits) return;

    const headers = authHeaders(token);

    const [farmsRes, fieldsRes, fruitsRes] = await Promise.all([
      needFarms  ? apiPom.get<FarmWithFields[]>('/farms/',  { headers }) : Promise.resolve({ data: farms }),
      needFields ? apiPom.get<Field[]>('/fields/',          { headers }) : Promise.resolve({ data: fields }),
      needFruits ? apiPom.get<Fruit[]>('/fruits/',          { headers }) : Promise.resolve({ data: fruits }),
    ]);

    const farmsData  = farmsRes.data  ?? farms;
    const fieldsData = fieldsRes.data ?? fields;
    const fruitsData = fruitsRes.data ?? fruits;

    setFarms(farmsData);
    setFields(fieldsData);
    setFruits(fruitsData);

    if (farmsData.length === 1) setActiveFarm(farmsData[0]);
  };

  return { fetchBootstrapData };
}
