import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, AlertTriangle, BookOpen, ArrowLeft, Loader2, Clock, CheckCircle2, AlertCircle } from 'lucide-react';
import { interviewApi } from '../api/interviewApi';

export default function ReportPage() {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchReport = async () => {
      setLoading(true);
      try {
        const data = await interviewApi.getReport(id);
        setReport(data);
      } catch (err) {
        setErrorMessage(err.message || 'Unable to load interview report.');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchReport();
    }
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-indigo-600 dark:text-amber-400" />
        <p className="text-sm opacity-70">Loading session summary & transcript...</p>
      </div>
    );
  }

  if (errorMessage || !report) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 space-y-4 text-center">
        <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-rose-800 space-y-3">
          <AlertCircle className="w-8 h-8 text-rose-600 mx-auto" />
          <h2 className="text-lg font-bold">Report Unavailable</h2>
          <p className="text-sm">{errorMessage || 'Session not found.'}</p>
          <div className="pt-2">
            <Link
              to="/dashboard"
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700"
            >
              Return to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const isCompleted = report.status === 'completed';

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-amber-400 hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </Link>
        <span className={`text-xs px-3 py-1 rounded-full font-semibold ${
          isCompleted
            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
            : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
        }`}>
          {isCompleted ? 'Session Completed' : 'Session In Progress'}
        </span>
      </div>

      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-black">Interview Session Summary</h1>
        <p className="text-sm opacity-70">
          Target Role: <strong>{report.job_title}</strong> • Session ID: <code className="text-xs bg-slate-100 dark:bg-zinc-800 px-1.5 py-0.5 rounded">{report.session_id}</code>
        </p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl space-y-1">
          <span className="text-xs font-bold uppercase opacity-60">Answered Questions</span>
          <div className="text-3xl font-black text-indigo-600 dark:text-amber-400">
            {report.completed_turns} / {report.total_questions}
          </div>
          <span className="text-xs opacity-70 block">
            {isCompleted ? 'All scheduled turns completed' : 'Session ended before completion'}
          </span>
        </div>

        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl space-y-1">
          <span className="text-xs font-bold uppercase opacity-60">Status</span>
          <div className="text-2xl font-bold capitalize pt-1">
            {report.status.replace('_', ' ')}
          </div>
          <span className="text-xs opacity-70 block">
            Recorded at {report.created_at ? new Date(report.created_at).toLocaleTimeString() : 'N/A'}
          </span>
        </div>

        <div className="p-6 bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl space-y-1">
          <span className="text-xs font-bold uppercase opacity-60">Accessibility Config</span>
          <div className="text-sm font-semibold pt-1 space-y-0.5">
            <div>Simplified Language: {report.accessibility_settings?.simplified_language ? 'Yes' : 'No'}</div>
            <div>Untimed Mode: {report.accessibility_settings?.extended_time ? 'Active' : 'Off'}</div>
          </div>
        </div>
      </div>

      {/* Q&A Transcript */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 sm:p-8 space-y-6">
        <div className="flex items-center justify-between border-b pb-4 border-slate-200 dark:border-zinc-800">
          <div>
            <h2 className="text-xl font-bold">Interview Transcript</h2>
            <p className="text-xs opacity-70">Review the technical questions delivered and your recorded text responses</p>
          </div>
          <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 dark:bg-zinc-800 rounded-lg">
            {report.transcript?.length || 0} Questions
          </span>
        </div>

        <div className="space-y-6">
          {report.transcript && report.transcript.length > 0 ? (
            report.transcript.map((item, index) => (
              <div key={index} className="p-5 rounded-2xl border border-slate-200 dark:border-zinc-800 space-y-3 bg-slate-50/50 dark:bg-zinc-950/40">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-amber-400">
                    Question {item.turn_index} • {item.topic_name}
                  </span>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-slate-200 dark:bg-zinc-800 capitalize">
                    {item.difficulty}
                  </span>
                </div>

                <div className="text-base font-semibold text-slate-900 dark:text-white leading-relaxed">
                  {item.question_text}
                </div>

                {item.simplified_question_text && (
                  <div className="text-xs text-slate-500 dark:text-zinc-400 italic">
                    Plain phrasing: {item.simplified_question_text}
                  </div>
                )}

                <div className="pt-2 border-t border-slate-200 dark:border-zinc-800 space-y-1">
                  <span className="text-xs font-bold uppercase opacity-60">Candidate Response:</span>
                  {item.candidate_answer ? (
                    <p className="text-sm text-slate-800 dark:text-zinc-200 whitespace-pre-wrap leading-relaxed bg-white dark:bg-zinc-900 p-3.5 rounded-xl border border-slate-200 dark:border-zinc-800">
                      {item.candidate_answer}
                    </p>
                  ) : (
                    <p className="text-xs text-amber-600 italic">No response submitted (skipped or ended early).</p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <p className="text-xs opacity-60">No transcript entries recorded.</p>
          )}
        </div>
      </div>

      {/* AI Evaluation Milestone Notice */}
      <div className="p-6 bg-indigo-50/70 border border-indigo-200 dark:bg-zinc-900 dark:border-amber-400/30 rounded-2xl space-y-2 text-sm">
        <div className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-indigo-600 dark:text-amber-400" />
          <span>Upcoming AI Evaluation & Roadmap Capabilities</span>
        </div>
        <p className="text-xs text-slate-600 dark:text-zinc-400 leading-relaxed">
          Full rubric scoring (relevance, technical depth, clarity), diagnostic skill gap identification,
          and tailored 2–4 week learning roadmaps will be generated once the Evaluation Agent and
          Skill Gap & Learning Agent are activated in Phases 10–13.
        </p>
      </div>

      {/* Bottom Actions */}
      <div className="flex justify-between items-center pt-2">
        <Link
          to="/dashboard"
          className="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-zinc-700 text-xs font-semibold hover:bg-slate-50 dark:hover:bg-zinc-800 transition-colors"
        >
          Back to Dashboard
        </Link>
        <Link
          to="/setup"
          className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl shadow transition-colors dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300"
        >
          Start Another Mock Interview
        </Link>
      </div>
    </div>
  );
}
