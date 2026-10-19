import React, { useState } from 'react';
import { Eye, HelpCircle, Volume2, CheckCircle2, Mic, Clock, Sparkles } from 'lucide-react';

export default function AccessibilityPreview() {
  const [highContrast, setHighContrast] = useState(false);
  const [fontSize, setFontSize] = useState('text-base'); // text-base, text-lg, text-xl
  const [simplified, setSimplified] = useState(false);
  const [activeTab, setActiveTab] = useState('intellectual');

  const standardQuestion = "Can you describe how the Python Global Interpreter Lock (GIL) affects thread execution for CPU-bound tasks compared to I/O-bound tasks?";
  const simplifiedQuestion = "What does Python's GIL do, and how is using threads different for CPU tasks versus waiting for network or disk tasks?";

  const accommodationTabs = [
    {
      id: 'intellectual',
      label: 'Intellectual Needs',
      badge: 'Cognitive Clarity',
      points: [
        'Option to view simplified, plain-language question phrasing',
        'Structured, step-by-step conceptual questions',
        'Extended response deliberation without stressful countdown timers'
      ]
    },
    {
      id: 'autism',
      label: 'Autism Spectrum (ASD)',
      badge: 'Predictability & Focus',
      points: [
        'Direct, unambiguous questions without idioms or metaphors',
        'Clear progress indicators showing remaining interview topics',
        'Clean, low-distraction interface with structured visual boundaries'
      ]
    },
    {
      id: 'deaf',
      label: 'Deaf / Hard of Hearing',
      badge: 'Visual Parity',
      points: [
        'Captions and on-screen text for all spoken questions',
        'Full text parity: every audio question is rendered in readable text',
        'Visual status badges for recording, evaluating, and next turns'
      ]
    },
    {
      id: 'speech',
      label: 'Speech Disabilities',
      badge: 'Communication Aware',
      points: [
        'Choice between voice dictation and typed text responses',
        'Designed for pause-tolerant speech input without mid-sentence cutoffs',
        'Evaluation designed to assess technical substance rather than speech fluency'
      ]
    }
  ];

  const currentTabData = accommodationTabs.find(t => t.id === activeTab);

  return (
    <div className="space-y-8">
      {/* Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-slate-100 rounded-2xl border border-slate-200">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            Interactive Accessibility Preview (Example):
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {/* High Contrast Toggle */}
          <button
            onClick={() => setHighContrast(prev => !prev)}
            aria-pressed={highContrast}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg border transition-colors flex items-center gap-1.5 ${
              highContrast
                ? 'bg-amber-400 text-black border-amber-500 shadow-sm'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span>High Contrast: {highContrast ? 'ON' : 'OFF'}</span>
          </button>

          {/* Font Size Selector */}
          <div className="inline-flex rounded-lg border border-slate-300 bg-white p-0.5 text-xs font-semibold">
            <button
              onClick={() => setFontSize('text-base')}
              className={`px-2.5 py-1 rounded ${fontSize === 'text-base' ? 'bg-indigo-600 text-white' : 'text-slate-600 hover:text-slate-900'}`}
            >
              16px
            </button>
            <button
              onClick={() => setFontSize('text-lg')}
              className={`px-2.5 py-1 rounded ${fontSize === 'text-lg' ? 'bg-indigo-600 text-white' : 'text-slate-600 hover:text-slate-900'}`}
            >
              18px
            </button>
            <button
              onClick={() => setFontSize('text-xl')}
              className={`px-2.5 py-1 rounded ${fontSize === 'text-xl' ? 'bg-indigo-600 text-white' : 'text-slate-600 hover:text-slate-900'}`}
            >
              22px
            </button>
          </div>

          {/* Simplified Phrasing Toggle */}
          <button
            onClick={() => setSimplified(prev => !prev)}
            aria-pressed={simplified}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg border transition-colors flex items-center gap-1.5 ${
              simplified
                ? 'bg-emerald-600 text-white border-emerald-700 shadow-sm'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            <span>Plain Phrasing: {simplified ? 'Active' : 'Standard'}</span>
          </button>
        </div>
      </div>

      {/* Simulated Interview Question Card */}
      <div
        className={`p-6 sm:p-8 rounded-3xl border transition-all duration-200 shadow-lg ${
          highContrast
            ? 'bg-black text-amber-300 border-amber-400'
            : 'bg-white text-slate-900 border-slate-200'
        }`}
      >
        <div className="flex items-center justify-between pb-4 border-b border-dashed border-slate-200 dark:border-amber-400/30">
          <div className="flex items-center gap-2">
            <span className={`px-2.5 py-1 text-xs font-bold rounded-full ${
              highContrast ? 'bg-amber-400 text-black' : 'bg-indigo-100 text-indigo-700'
            }`}>
              Sample Turn • Python Internals
            </span>
            <span className={`text-xs font-semibold ${highContrast ? 'text-amber-200' : 'text-slate-500'}`}>
              Difficulty: Medium
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className={`text-xs px-2 py-0.5 rounded border ${
              highContrast ? 'border-amber-400 text-amber-300' : 'border-slate-300 text-slate-600'
            }`}>
              Untimed Mode
            </span>
          </div>
        </div>

        <div className="py-6 space-y-4">
          <div className="flex items-start justify-between gap-4">
            <p className={`${fontSize} font-bold leading-relaxed transition-all`}>
              {simplified ? simplifiedQuestion : standardQuestion}
            </p>
            <div className={`p-2 rounded-xl border flex-shrink-0 ${
              highContrast ? 'border-amber-400 text-amber-300' : 'border-slate-200 text-indigo-600'
            }`}>
              <Volume2 className="w-5 h-5" />
            </div>
          </div>

          {simplified && (
            <div className={`p-3 rounded-xl text-xs font-medium ${
              highContrast ? 'bg-zinc-900 border border-amber-400 text-amber-200' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
            }`}>
              Example of simplified wording. Technical expectations remain the same: candidate explains the GIL and thread vs process differences.
            </div>
          )}
        </div>

        {/* Live Accessibility Indicator Footnote */}
        <div className="pt-4 border-t border-dashed border-slate-200 dark:border-amber-400/30 flex flex-wrap items-center justify-between text-xs gap-3">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 opacity-80">
              <Mic className="w-3.5 h-3.5 text-emerald-500" /> Planned: Pause-tolerant speech input
            </span>
            <span className="flex items-center gap-1.5 opacity-80">
              <Clock className="w-3.5 h-3.5 text-indigo-500" /> Untimed mode preview
            </span>
          </div>
          <span className="opacity-70 font-mono text-[11px]">Alt+S to Submit • Alt+R to Repeat</span>
        </div>
      </div>

      {/* Target Audience Accommodations Matrix */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div className="space-y-1">
          <h3 className="text-xl font-bold text-slate-900">Accessibility Support for Common Needs</h3>
          <p className="text-sm text-slate-600">
            AccessHire AI includes configurable settings designed to support common cognitive, sensory, and communication preferences:
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-3">
          {accommodationTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 text-xs font-bold rounded-xl transition-all ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white shadow'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Active Tab Details */}
        <div className="bg-indigo-50/50 border border-indigo-100 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-slate-900 text-base">{currentTabData.label}</h4>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-100 text-indigo-700">
              {currentTabData.badge}
            </span>
          </div>
          <ul className="space-y-2.5 text-sm text-slate-700">
            {currentTabData.points.map((pt, i) => (
              <li key={i} className="flex items-center gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <span>{pt}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
