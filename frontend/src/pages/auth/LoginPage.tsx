import { FormEvent, useState } from 'react';

import { useAuth } from '../../hooks/useAuth';

export function LoginPage() {
  const { login, logout, loadProfile, user } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage('');
    try {
      await login(email, password);
      setMessage('Login successful.');
    } catch {
      setMessage('Login failed.');
    }
  }

  return (
    <div>
      <form onSubmit={onSubmit}>
        <h1>Login</h1>
        <label>
          Email
          <input value={email} onChange={(event) => setEmail(event.target.value)} />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <button type="submit">Log in</button>
      </form>

      <button type="button" onClick={() => void loadProfile()}>
        Refresh profile
      </button>
      <button type="button" onClick={() => void logout()}>
        Log out
      </button>

      {user ? (
        <p>
          Signed in as {user.email} ({user.role})
        </p>
      ) : (
        <p>Not signed in</p>
      )}

      {message ? <p>{message}</p> : null}
    </div>
  );
}
