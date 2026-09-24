import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Placeholder register - navigates to dashboard
    navigate('/dashboard');
  };

  return (
    <div className="max-w-md mx-auto my-16 p-8 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/40 rounded-2xl shadow-sm space-y-6">
      <div className="space-y-2 text-center">
        <h1 className="text-2xl font-bold">Create Account</h1>
        <p className="text-sm text-slate-500">Join AccessHire AI for accessible mock interview practice</p>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1" htmlFor="name">Full Name</label>
          <input
            id="name"
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-black dark:border-amber-400"
            placeholder="Alex Smith"
          />
        </div>
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider mb-1" htmlFor="email">Email Address</label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-black dark:border-amber-400"
            placeholder="alex@example.com"
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
          />
        </div>
        <button
          type="submit"
          className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow transition-colors dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300"
        >
          Create Candidate Account
        </button>
      </form>
      <div className="text-center text-xs text-slate-500">
        Already registered? <Link to="/login" className="text-indigo-600 dark:text-amber-400 font-semibold underline">Sign in</Link>
      </div>
    </div>
  );
}
