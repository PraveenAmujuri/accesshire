import React, { createContext, useContext, useState, useEffect } from 'react';

const AccessibilityContext = createContext();

export function AccessibilityProvider({ children }) {
  const [highContrast, setHighContrast] = useState(false);
  const [fontSize, setFontSize] = useState('text-base'); // 'text-sm', 'text-base', 'text-lg', 'text-xl'

  const toggleHighContrast = () => setHighContrast(prev => !prev);

  return (
    <AccessibilityContext.Provider value={{ highContrast, toggleHighContrast, fontSize, setFontSize }}>
      <div className={`${highContrast ? 'bg-black text-amber-300 contrast-mode' : 'bg-slate-50 text-slate-900'} ${fontSize} min-h-screen transition-colors duration-200`}>
        {children}
      </div>
    </AccessibilityContext.Provider>
  );
}

export const useAccessibility = () => useContext(AccessibilityContext);
