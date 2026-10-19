import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PlusCircle, BarChart3, Clock, PlayCircle, Loader2, AlertCircle } from 'lucide-react';
import { interviewApi } from '../api/interviewApi';

export default function DashboardPage() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchSessions = async () => {
      setLoading(true);
      try {
        const data = await interviewApi.listSessions();
        setSessions(Array.isArray(data) ? data : []);
      } catch (err) {
        setErrorMessage(err.message || 'Failed to load past sessions.');
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, []);

  const completedCount = sessions.filter(s => s.status === 'completed').length;
  const inProgressCount = sessions.filter(s => s.status === 'in_progress').length;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold">Candidate Dashboard</h1>
          <p className="text-sm opacity-70">Track your interview practice sessions and review transcripts</p>
        </div>
        <Link
          to="/setup"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow transition-colors dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300"
        >
          <PlusCircle className="w-5 h-5" />
          <span>New Practice Interview</span>
        </Link>
      </div>

      {errorMessage && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-amber-600" />
          <span>{errorMessage} (Make sure the backend server is running on http://localhost:8000)</span>
        </div>
      )}

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl">
          <div className="text-xs uppercase font-bold opacity-60">Completed Sessions</div>
          <div className="text-3xl font-black mt-2 text-indigo-600 dark:text-amber-400">
            {completedCount}
          </div>
        </div>
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl">
          <div className="text-xs uppercase font-bold opacity-60">In-Progress Sessions</div>
          <div className="text-3xl font-black mt-2 text-amber-600 dark:text-amber-400">
            {inProgressCount}
          </div>
        </div>
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl">
          <div className="text-xs uppercase font-bold opacity-60">Session Storage Mode</div>
          <div className="text-base font-bold mt-2 text-emerald-600 dark:text-emerald-400">
            MongoDB / Local Store Active
          </div>
        </div>
      </div>

      {/* Past Sessions List */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between border-b pb-3 border-slate-100 dark:border-zinc-800">
          <h2 className="text-xl font-bold">Interview Sessions</h2>
          <span className="text-xs opacity-60">{sessions.length} Recorded</span>
        </div>

        {loading ? (
          <div className="py-12 text-center space-y-2">
            <Loader2 className="w-6 h-6 animate-spin mx-auto text-indigo-600 dark:text-amber-400" />
            <p className="text-xs opacity-60">Loading sessions...</p>
          </div>
        ) : sessions.length === 0 ? (
          <div className="py-12 text-center space-y-3">
            <p className="text-sm opacity-70">You haven't conducted any mock interview sessions yet.</p>
            <Link
              to="/setup"
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Configure Your First Interview</span>
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-slate-100 dark:divide-zinc-800">
            {sessions.map((item) => (
              <div key={item.session_id} className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div className="space-y-0.5">
                  <div className="font-semibold text-base">{item.job_title}</div>
                  <div className="flex items-center gap-3 text-xs opacity-60">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {item.created_at ? new Date(item.created_at).toLocaleDateString() : 'Recent'}
                    </span>
                    <span>•</span>
                    <span>Progress: {item.current_turn} of {item.total_questions}</span>
                    <span>•</span>
                    <span className="capitalize font-medium">{item.status.replace('_', ' ')}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {item.status === 'in_progress' ? (
                    <Link
                      to={`/interview/${item.session_id}`}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-indigo-50 text-indigo-700 hover:bg-indigo-100 dark:bg-zinc-800 dark:text-amber-400 transition-colors"
                    >
                      <PlayCircle className="w-4 h-4" />
                      <span>Resume Interview</span>
                    </Link>
                  ) : (
                    <Link
                      to={`/report/${item.session_id}`}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg border border-slate-300 dark:border-amber-400 hover:bg-slate-50 dark:hover:bg-zinc-800 transition-colors"
                    >
                      <BarChart3 className="w-4 h-4" />
                      <span>View Transcript & Report</span>
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
