import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-600 rounded p-1">
          <div className="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center text-white shadow">
            <Sparkles className="w-5 h-5" />
          </div>
          <span>AccessHire <span className="text-indigo-600">AI</span></span>
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-600">
          <Link to="/" className="hover:text-indigo-600 transition-colors focus:ring-2 focus:ring-indigo-600 rounded px-2 py-1">Home</Link>
          <Link to="/features" className="hover:text-indigo-600 transition-colors focus:ring-2 focus:ring-indigo-600 rounded px-2 py-1">Features</Link>
          <Link to="/about" className="hover:text-indigo-600 transition-colors focus:ring-2 focus:ring-indigo-600 rounded px-2 py-1">Architecture</Link>
        </nav>
        <div className="flex items-center gap-3">
          <a
            href="http://localhost:5174/login"
            className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-indigo-600 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-600 rounded-lg"
          >
            Sign In
          </a>
          <a
            href="http://localhost:5174/register"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 transition-colors rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600"
          >
            <span>Start Practice</span>
            <ArrowRight className="w-4 h-4" />
          </a>
        </div>
      </div>
    </header>
  );
}
