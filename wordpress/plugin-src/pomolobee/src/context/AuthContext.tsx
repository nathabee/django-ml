// src/context/AuthContext.tsx
'use client';

import React, { createContext, useContext, useEffect, useState } from "react";
import { User } from "@mytypes/user";
import { FarmWithFields } from "@mytypes/farm";
import { Field, FieldBasic } from "@mytypes/field";

type Maybe<T> = T | null;

type AuthContextType = {
  // auth
  token: Maybe<string>;
  user: Maybe<User>;
  isLoggedIn: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  setToken: (t: Maybe<string>) => void;

  // domain
  farms: FarmWithFields[];            // all farms visible to the user (admin sees many)
  setFarms: (f: FarmWithFields[]) => void;

  activeFarm: Maybe<FarmWithFields>;
  setActiveFarm: (f: Maybe<FarmWithFields>) => void;

  activeField: Maybe<FieldBasic | Field>;
  setActiveField: (f: Maybe<FieldBasic | Field>) => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setTokenState] = useState<Maybe<string>>(null);
  const [user, setUser] = useState<Maybe<User>>(null);
  const [farms, setFarmsState] = useState<FarmWithFields[]>([]);
  const [activeFarm, setActiveFarmState] = useState<Maybe<FarmWithFields>>(null);
  const [activeField, setActiveFieldState] = useState<Maybe<FieldBasic | Field>>(null);

  const isLoggedIn = !!token;

  // boot from localStorage
  useEffect(() => {
    if (typeof window === "undefined") return;
    const t = localStorage.getItem("authToken");
    const u = localStorage.getItem("userInfo");
    const fs = localStorage.getItem("farms");
    const af = localStorage.getItem("activeFarm");
    const fld = localStorage.getItem("activeField");

    if (t) setTokenState(t);
    if (u) setUser(JSON.parse(u));
    if (fs) setFarmsState(JSON.parse(fs));
    if (af) setActiveFarmState(JSON.parse(af));
    if (fld) setActiveFieldState(JSON.parse(fld));
  }, []);

  // persist
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (token) localStorage.setItem("authToken", token);
    else localStorage.removeItem("authToken");
  }, [token]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (user) localStorage.setItem("userInfo", JSON.stringify(user));
    else localStorage.removeItem("userInfo");
  }, [user]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    localStorage.setItem("farms", JSON.stringify(farms));
  }, [farms]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (activeFarm) localStorage.setItem("activeFarm", JSON.stringify(activeFarm));
    else localStorage.removeItem("activeFarm");
  }, [activeFarm]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (activeField) localStorage.setItem("activeField", JSON.stringify(activeField));
    else localStorage.removeItem("activeField");
  }, [activeField]);

  const login = (tok: string, u: User) => {
    setTokenState(tok);
    setUser(u);
  };

  const logout = () => {
    setTokenState(null);
    setUser(null);
    setFarmsState([]);
    setActiveFarmState(null);
    setActiveFieldState(null);
    if (typeof window !== "undefined") {
      localStorage.clear(); // simple reset for MVP
    }
  };

  const setToken = (t: Maybe<string>) => setTokenState(t);
  const setFarms = (f: FarmWithFields[]) => setFarmsState(f);
  const setActiveFarm = (f: Maybe<FarmWithFields>) => {
    setActiveFarmState(f);
    // when switching farm, clear field selection
    setActiveFieldState(null);
  };
  const setActiveField = (f: Maybe<FieldBasic | Field>) => setActiveFieldState(f);

  return (
    <AuthContext.Provider value={{
      token, user, isLoggedIn, login, logout, setToken,
      farms, setFarms,
      activeFarm, setActiveFarm,
      activeField, setActiveField,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
