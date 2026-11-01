import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { interviewApi } from '../api/interviewApi';
import { LogIn, AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await interviewApi.login({ email, password });
      if (response && response.access_token) {
        localStorage.setItem('accesshire_token', response.access_token);
        localStorage.setItem('accesshire_user', JSON.stringify({
          id: response.user_id,
          email: response.email,
          name: response.full_name,
        }));
        navigate('/dashboard');
      } else {
        setError('Login failed: Token not received');
      }
    } catch (err) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto my-16 p-8 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/40 rounded-2xl shadow-sm space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Candidate Sign In</h1>
        <p className="text-sm text-slate-500">Access your adaptive mock interviews and roadmaps</p>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 rounded-lg text-sm">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1" htmlFor="email">Email Address</label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-black dark:border-amber-400"
            placeholder="candidate@example.com"
            disabled={loading}
          />
        </div>
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1" htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-black dark:border-amber-400"
            placeholder="••••••••"
            disabled={loading}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold rounded-lg shadow transition-colors dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300 flex items-center justify-center gap-2"
        >
          <LogIn className="w-4 h-4" />
          <span>{loading ? 'Signing In...' : 'Sign In'}</span>
        </button>
      </form>
      <div className="text-center text-xs text-slate-500">
        Don't have an account? <Link to="/register" className="text-indigo-600 dark:text-amber-400 font-semibold underline">Register here</Link>
      </div>
    </div>
  );
}
