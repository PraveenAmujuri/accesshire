import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, Eye, Type, User, LogOut } from 'lucide-react';
import { useAccessibility } from '../context/AccessibilityContext';

export default function Navbar() {
  const { highContrast, toggleHighContrast, fontSize, setFontSize } = useAccessibility();
  const navigate = useNavigate();
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const rawUser = localStorage.getItem('accesshire_user');
    const token = localStorage.getItem('accesshire_token');
    if (rawUser && token) {
      try {
        setCurrentUser(JSON.parse(rawUser));
      } catch (e) {
        setCurrentUser(null);
      }
    } else {
      setCurrentUser(null);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accesshire_token');
    localStorage.removeItem('accesshire_user');
    setCurrentUser(null);
    navigate('/login');
  };

  const cycleFontSize = () => {
    if (fontSize === 'text-sm') setFontSize('text-base');
    else if (fontSize === 'text-base') setFontSize('text-lg');
    else if (fontSize === 'text-lg') setFontSize('text-xl');
    else setFontSize('text-sm');
  };

  return (
    <header className={`sticky top-0 z-50 border-b ${highContrast ? 'bg-black border-amber-400 text-amber-300' : 'bg-white/95 backdrop-blur border-slate-200 text-slate-900'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl focus:outline-none focus:ring-2 focus:ring-amber-400 rounded p-1">
          <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${highContrast ? 'bg-amber-400 text-black' : 'bg-indigo-600 text-white'}`}>
            <Sparkles className="w-4 h-4" />
          </div>
          <span>AccessHire <span className={highContrast ? 'text-amber-400' : 'text-indigo-600'}>Interview</span></span>
        </Link>

        <nav className="flex items-center gap-4 text-sm font-medium">
          <Link to="/dashboard" className="hover:underline focus:ring-2 focus:ring-amber-400 p-1 rounded">Dashboard</Link>
          <Link to="/setup" className="hover:underline focus:ring-2 focus:ring-amber-400 p-1 rounded">New Interview</Link>
        </nav>

        {/* Accessibility & Account Toolbar */}
        <div className="flex items-center gap-3">
          <button
            onClick={toggleHighContrast}
            aria-label="Toggle High Contrast Theme"
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg border transition-colors ${
              highContrast ? 'border-amber-400 bg-amber-400 text-black' : 'border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span>{highContrast ? 'Contrast: ON' : 'High Contrast'}</span>
          </button>

          <button
            onClick={cycleFontSize}
            aria-label="Adjust Text Size"
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg border transition-colors ${
              highContrast ? 'border-amber-400 text-amber-300 hover:bg-zinc-900' : 'border-slate-300 bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <Type className="w-3.5 h-3.5" />
            <span>Size: {fontSize.replace('text-', '')}</span>
          </button>

          {currentUser ? (
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium px-2 py-1 rounded bg-slate-100 dark:bg-zinc-800 border border-slate-200 dark:border-amber-400/30">
                {currentUser.name || currentUser.email}
              </span>
              <button
                onClick={handleLogout}
                className={`p-2 rounded-lg border transition-colors ${
                  highContrast ? 'border-amber-400 text-amber-300 hover:bg-zinc-900' : 'border-slate-200 text-slate-700 hover:bg-slate-100'
                }`}
                title="Log out"
                aria-label="Log out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <Link
              to="/login"
              className={`p-2 rounded-lg border transition-colors ${
                highContrast ? 'border-amber-400 text-amber-300 hover:bg-zinc-900' : 'border-slate-200 text-slate-700 hover:bg-slate-100'
              }`}
              title="User Account"
            >
              <User className="w-4 h-4" />
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
