import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Briefcase, Sliders, Play } from 'lucide-react';

export default function SetupPage() {
  const navigate = useNavigate();
  const [jobTitle, setJobTitle] = useState('Junior AI Engineer');
  const [jobDescription, setJobDescription] = useState('');
  const [simplifiedLanguage, setSimplifiedLanguage] = useState(false);
  const [extendedTime, setExtendedTime] = useState(true);

  const handleStartInterview = (e) => {
    e.preventDefault();
    // Navigates to the live interview room
    navigate('/interview/demo_session_1');
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold">Configure Interview Session</h1>
        <p className="text-sm opacity-70">Upload your resume, target job description, and set accessibility accommodations</p>
      </div>

      <form onSubmit={handleStartInterview} className="space-y-8">
        {/* Resume upload placeholder */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Upload className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>1. Resume File (PDF / DOCX)</span>
          </div>
          <p className="text-xs opacity-70">PyMuPDF and python-docx document parsers will extract candidate skills and history.</p>
          <div className="border-2 border-dashed border-slate-300 dark:border-zinc-700 rounded-xl p-6 text-center hover:border-indigo-500 transition-colors cursor-pointer">
            <span className="text-sm font-medium">Drag & drop your resume here, or click to browse</span>
          </div>
        </div>

        {/* Job description input */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Briefcase className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>2. Target Job Description</span>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="jobTitle">Job Title</label>
            <input
              id="jobTitle"
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm"
              placeholder="e.g. Junior AI Engineer"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="jd">Job Description Text</label>
            <textarea
              id="jd"
              rows={4}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm font-mono"
              placeholder="Paste job description requirements and responsibilities here..."
            />
          </div>
        </div>

        {/* Accessibility preferences */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Sliders className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>3. Accessibility Accommodations</span>
          </div>
          <div className="space-y-3">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={simplifiedLanguage}
                onChange={(e) => setSimplifiedLanguage(e.target.checked)}
                className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
              />
              <div>
                <div className="text-sm font-semibold">Simplified Question Phrasing</div>
                <div className="text-xs opacity-70">Provides plain-language question alternatives without lowering technical rigor</div>
              </div>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={extendedTime}
                onChange={(e) => setExtendedTime(e.target.checked)}
                className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
              />
              <div>
                <div className="text-sm font-semibold">Extended / Untimed Response Mode</div>
                <div className="text-xs opacity-70">Disables strict countdown timers to support thoughtful deliberation</div>
              </div>
            </label>
          </div>
        </div>

        <button
          type="submit"
          className="w-full py-3.5 px-6 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300"
        >
          <Play className="w-5 h-5" />
          <span>Generate Plan & Start Mock Interview</span>
        </button>
      </form>
    </div>
  );
}
