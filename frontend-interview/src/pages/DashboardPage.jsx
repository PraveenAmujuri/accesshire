import React from 'react';
import { Link } from 'react-router-dom';
import { PlusCircle, PlayCircle, BarChart3, Clock } from 'lucide-react';

export default function DashboardPage() {
  const dummyInterviews = [
    { id: 'sess_101', role: 'Junior AI Engineer', date: 'Yesterday', score: '82%', status: 'Completed' },
    { id: 'sess_102', role: 'Full Stack Developer', date: '3 days ago', score: '74%', status: 'Completed' },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold">Candidate Dashboard</h1>
          <p className="text-sm opacity-70">Track your interview sessions, progress, and skill development</p>
        </div>
        <Link
          to="/setup"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow transition-colors dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300"
        >
          <PlusCircle className="w-5 h-5" />
          <span>New Practice Interview</span>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl">
          <div className="text-xs uppercase font-bold opacity-60">Completed Sessions</div>
          <div className="text-3xl font-black mt-2">2</div>
        </div>
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl">
          <div className="text-xs uppercase font-bold opacity-60">Average Competency Score</div>
          <div className="text-3xl font-black mt-2 text-indigo-600 dark:text-amber-400">78%</div>
        </div>
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl">
          <div className="text-xs uppercase font-bold opacity-60">Adaptive Mode</div>
          <div className="text-3xl font-black mt-2 text-emerald-600 dark:text-emerald-400">Active</div>
        </div>
      </div>

      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
        <h2 className="text-xl font-bold">Past Interview Sessions</h2>
        <div className="divide-y divide-slate-100 dark:divide-zinc-800">
          {dummyInterviews.map((item) => (
            <div key={item.id} className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <div>
                <div className="font-semibold text-lg">{item.role}</div>
                <div className="flex items-center gap-3 text-xs opacity-60 mt-0.5">
                  <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {item.date}</span>
                  <span>•</span>
                  <span>Score: <strong className="text-indigo-600 dark:text-amber-400">{item.score}</strong></span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Link
                  to={`/report/${item.id}`}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-300 dark:border-amber-400 hover:bg-slate-50 dark:hover:bg-zinc-800 transition-colors"
                >
                  <BarChart3 className="w-4 h-4" />
                  <span>Report & Roadmap</span>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
