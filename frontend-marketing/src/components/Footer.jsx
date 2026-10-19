import React from 'react';
import { Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <span className="text-white font-bold text-lg">AccessHire AI</span>
            <p className="text-xs text-slate-400 mt-1">
              Accessible mock interview platform with adaptive question practice.
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <span>Adaptive interview practice</span>
            <span>•</span>
            <span className="flex items-center gap-1">Designed for Accessibility <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" /></span>
          </div>
        </div>
      </div>
    </footer>
  );
}
