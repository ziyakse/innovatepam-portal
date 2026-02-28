import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react';

type Role = 'submitter' | 'evaluator_admin';

type UserProfile = {
  id: string;
  email: string;
  role: Role;
};

type AuthResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: UserProfile;
};

type AuthContextValue = {
  user: UserProfile | null;
  accessToken: string | null;
  refreshToken: string | null;
  register: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loadProfile: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

const API_BASE = 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

  async function register(email: string, password: string) {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }
  }

  async function login(email: string, password: string) {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const auth = (await response.json()) as AuthResponse;
    setAccessToken(auth.access_token);
    setRefreshToken(auth.refresh_token);
    setUser(auth.user);
  }

  async function logout() {
    if (!accessToken || !refreshToken) {
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      return;
    }

    await fetch(`${API_BASE}/auth/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);
  }

  async function loadProfile() {
    if (!accessToken) {
      return;
    }

    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        setUser(null);
        setAccessToken(null);
        setRefreshToken(null);
      }
      return;
    }

    const profile = (await response.json()) as UserProfile;
    setUser(profile);
  }

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      accessToken,
      refreshToken,
      register,
      login,
      logout,
      loadProfile,
    }),
    [user, accessToken, refreshToken],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
