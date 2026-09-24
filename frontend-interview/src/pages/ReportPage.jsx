import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, AlertTriangle, BookOpen, ArrowLeft } from 'lucide-react';

export default function ReportPage() {
  const { id } = useParams();

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="flex items-center justify-between">
        <Link to="/dashboard" className="inline-flex items-center gap-1 text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-amber-400 hover:underline">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </Link>
        <span className="text-xs px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-semibold">
          Finalized Evaluation
        </span>
      </div>

      <div className="space-y-2">
        <h1 className="text-3xl font-black">Performance Diagnostics & Roadmap</h1>
        <p className="text-sm opacity-70">Session Reference: {id}</p>
      </div>

      {/* Overall Score */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl md:col-span-1 text-center flex flex-col items-center justify-center">
          <span className="text-xs font-bold uppercase opacity-60">Overall Score</span>
          <div className="text-5xl font-black text-indigo-600 dark:text-amber-400 my-2">78%</div>
          <span className="text-xs font-semibold text-emerald-600">Competency Passed</span>
        </div>
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl md:col-span-3 space-y-3">
          <h2 className="text-lg font-bold">Feedback Summary</h2>
          <p className="text-sm opacity-80 leading-relaxed">
            Demonstrated strong conceptual grasp of Python runtime mechanics and API architecture. Showed solid reasoning when follow-up probes were triggered by the Decision Policy Agent.
          </p>
        </div>
      </div>

      {/* Skill Gap Analysis */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <span>Identified Skill Gaps</span>
        </h2>
        <div className="space-y-3">
          <div className="p-4 bg-amber-50 dark:bg-zinc-800/80 border border-amber-200 dark:border-amber-400/30 rounded-xl text-sm">
            <strong className="block text-amber-900 dark:text-amber-300">Multi-processing vs AsyncIO Bottlenecks</strong>
            <span className="text-xs opacity-80">Answer omitted practical examples of bypassing GIL using multiprocessing for CPU-bound matrix tasks.</span>
          </div>
        </div>
      </div>

      {/* Learning Roadmap */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
          <span>Personalized Learning Roadmap</span>
        </h2>
        <div className="space-y-3">
          <div className="p-4 border border-slate-200 dark:border-zinc-800 rounded-xl space-y-1">
            <div className="text-xs font-bold uppercase text-indigo-600 dark:text-amber-400">Week 1: Advanced Concurrency</div>
            <div className="text-sm font-semibold">Master ProcessPoolExecutor and CPU-bound parallelization</div>
            <div className="text-xs opacity-70">Estimated completion time: 4 hours</div>
          </div>
        </div>
      </div>
    </div>
  );
}
