import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Briefcase, Sliders, Play, AlertCircle, Loader2 } from 'lucide-react';
import { interviewApi } from '../api/interviewApi';

export default function SetupPage() {
  const navigate = useNavigate();
  const [jobTitle, setJobTitle] = useState('Python Backend Developer');
  const [jobDescription, setJobDescription] = useState('Developing scalable REST APIs using FastAPI, async/await, and database integration.');
  const [targetQuestionCount, setTargetQuestionCount] = useState(3);
  const [simplifiedLanguage, setSimplifiedLanguage] = useState(false);
  const [extendedTime, setExtendedTime] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleStartInterview = async (e) => {
    e.preventDefault();
    if (!jobTitle.trim()) {
      setErrorMessage('Please provide a job title or target role.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const session = await interviewApi.startSession({
        job_title: jobTitle.trim(),
        job_description: jobDescription.trim(),
        target_question_count: Number(targetQuestionCount) || 3,
        simplified_language: simplifiedLanguage,
        extended_time: extendedTime,
        voice_enabled: false,
      });

      if (session && session.session_id) {
        navigate(`/interview/${session.session_id}`);
      } else {
        throw new Error('Session creation did not return a valid session ID.');
      }
    } catch (err) {
      setErrorMessage(err.message || 'Failed to initialize interview session.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold">Configure Interview Session</h1>
        <p className="text-sm opacity-70">Specify your target job role and customize your accessibility settings</p>
      </div>

      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-2.5">
          <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-600 mt-0.5" />
          <div>
            <strong className="block font-semibold">Unable to Start Session</strong>
            <span>{errorMessage}</span>
          </div>
        </div>
      )}

      <form onSubmit={handleStartInterview} className="space-y-8">
        {/* 1. Job Description & Role */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Briefcase className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>1. Target Job Role & Description</span>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="jobTitle">Job Title / Role</label>
            <input
              id="jobTitle"
              type="text"
              required
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="e.g. Python Backend Developer"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="jd">Job Description / Key Requirements</label>
            <textarea
              id="jd"
              rows={4}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm font-mono focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="Paste job description requirements, technical stack, and responsibilities..."
            />
          </div>
          <div className="pt-1">
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="count">Number of Questions</label>
            <select
              id="count"
              value={targetQuestionCount}
              onChange={(e) => setTargetQuestionCount(Number(e.target.value))}
              className="px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
            >
              <option value={2}>2 Questions (Quick Practice)</option>
              <option value={3}>3 Questions (Standard)</option>
              <option value={5}>5 Questions (In-depth)</option>
            </select>
          </div>
        </div>

        {/* 2. Resume Placeholder */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-3">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Upload className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>2. Candidate Resume (Optional for Phase 3)</span>
          </div>
          <p className="text-xs opacity-70">
            Resume parsing and skills extraction will be integrated via the Candidate & Job Analysis Agent in Phase 6.
          </p>
          <div className="border-2 border-dashed border-slate-300 dark:border-zinc-700 rounded-xl p-5 text-center text-xs opacity-70">
            Resume upload will be enabled in upcoming milestones. The session will currently calibrate from your job role.
          </div>
        </div>

        {/* 3. Accessibility Settings */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Sliders className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>3. Accessibility Settings</span>
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
          disabled={loading}
          className={`w-full py-3.5 px-6 font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 ${
            loading
              ? 'bg-indigo-400 cursor-not-allowed text-white'
              : 'bg-indigo-600 hover:bg-indigo-700 text-white dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Creating Session...</span>
            </>
          ) : (
            <>
              <Play className="w-5 h-5" />
              <span>Start Mock Interview</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
