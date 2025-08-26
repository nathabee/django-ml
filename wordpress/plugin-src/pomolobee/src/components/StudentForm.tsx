'use client';

import React, { useEffect, useState } from 'react';
import { Eleve } from '@mytypes/eleve';
import { User } from '@mytypes/user';
import { useAuth } from '@context/AuthContext';
import { getToken , isTokenExpired } from '@utils/jwt';
import { getApiUrl } from '@utils/helper';

interface StudentFormProps {
  setStudents: React.Dispatch<React.SetStateAction<Eleve[]>>;
  closeForm: () => void;
}

const StudentForm: React.FC<StudentFormProps> = ({ setStudents, closeForm }) => {
  const { user, niveaux } = useAuth();
  const [lastName, setLastName] = useState('');
  const [firstName, setFirstName] = useState('');
  const [level, setLevel] = useState('');
  const [birthDate, setBirthDate] = useState(() =>
    new Date(new Date().setFullYear(new Date().getFullYear() - 5)).toISOString().split('T')[0]
  );
  const [availableTeachers, setAvailableTeachers] = useState<User[]>([]);
  const [selectedTeachers, setSelectedTeachers] = useState<string[]>([]);

  useEffect(() => {
    const fetchTeachers = async () => {
      const token = getToken();
      if (!token || isTokenExpired(token)) return;

      try {
        const res = await fetch(`${getApiUrl()}/users/?role=teacher`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();
        setAvailableTeachers(data);
      } catch (e) {
        console.error('Failed to load teachers', e);
      }
    };

    if (user?.roles.includes('admin')) fetchTeachers();
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = getToken();
    if (!token || isTokenExpired(token)) return;

    const payload = {
      nom: lastName,
      prenom: firstName,
      niveau: level,
      datenaissance: birthDate,
      ...(user?.roles.includes('admin') && { professeurs: selectedTeachers })
    };

    try {
      const res = await fetch(`${getApiUrl()}/eleves/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const newStudent: Student = await res.json();
      setStudents(prev => [...prev, newStudent]);
      closeForm();
    } catch (err) {
      console.error('Failed to create student', err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create a Student</h2>

      <input className="form-control mb-2" type="text" value={lastName} onChange={e => setLastName(e.target.value)} placeholder="Last Name" required />
      <input className="form-control mb-2" type="text" value={firstName} onChange={e => setFirstName(e.target.value)} placeholder="First Name" required />

      <select className="form-control mb-2" value={level} onChange={e => setLevel(e.target.value)} required>
        <option value="" disabled>Select Level</option>
        {niveaux?.map(n => <option key={n.id} value={n.id}>{n.description}</option>)}
      </select>

      <input className="form-control mb-2" type="date" value={birthDate} onChange={e => setBirthDate(e.target.value)} required />

      {user?.roles.includes('admin') && (
        <select className="form-control mb-3" multiple onChange={e => setSelectedTeachers(Array.from(e.target.selectedOptions, opt => opt.value))}>
          {availableTeachers.map(t => (
            <option key={t.id} value={t.id}>{t.first_name} {t.last_name}</option>
          ))}
        </select>
      )}

      <button className="btn btn-primary" type="submit">Create Student</button>
    </form>
  );
};

export default StudentForm;
