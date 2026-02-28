import { FormEvent, useState } from 'react';

import { useAuth } from '../../hooks/useAuth';

export function RegisterPage() {
  const { register } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage('');
    try {
      await register(email, password);
      setMessage('Registration successful. You can now log in.');
    } catch {
      setMessage('Registration failed. Please try again.');
    }
  }

  return (
    <form onSubmit={onSubmit}>
      <h1>Register</h1>
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
      <button type="submit">Create account</button>
      {message ? <p>{message}</p> : null}
    </form>
  );
}
