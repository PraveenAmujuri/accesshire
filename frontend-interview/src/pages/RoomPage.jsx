import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Send, RotateCcw, Volume2, HelpCircle, CheckCircle } from 'lucide-react';

export default function RoomPage() {
  const { id } = useParams();
  const [answerText, setAnswerText] = useState('');
  const [simplifiedView, setSimplifiedView] = useState(false);

  const sampleQuestion = "Can you explain how the Python Global Interpreter Lock (GIL) impacts multi-threaded CPU-bound tasks versus I/O-bound tasks?";
  const sampleSimplified = "What does Python's GIL do, and how does it change how fast CPU and I/O tasks run when using threads?";

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top status bar */}
      <div className="flex items-center justify-between border-b pb-4 border-slate-200 dark:border-amber-400/30">
        <div>
          <span className="text-xs uppercase font-bold tracking-wider text-indigo-600 dark:text-amber-400">Adaptive Turn 1 of 6</span>
          <h2 className="text-lg font-bold">Topic: Python Concurrency & Architecture</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
            Difficulty: Medium
          </span>
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/40 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-start justify-between gap-4">
          <h1 className="text-xl font-bold leading-relaxed">
            {simplifiedView ? sampleSimplified : sampleQuestion}
          </h1>
          <button
            title="Read Question Aloud (Voice Output)"
            className="p-2.5 rounded-xl border border-slate-200 dark:border-amber-400 hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors"
          >
            <Volume2 className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
          </button>
        </div>

        <div className="flex items-center gap-3 pt-2">
          <button
            onClick={() => setSimplifiedView(prev => !prev)}
            className="text-xs font-semibold text-indigo-600 dark:text-amber-400 hover:underline flex items-center gap-1"
          >
            <HelpCircle className="w-3.5 h-3.5" />
            <span>{simplifiedView ? "Show original phrasing" : "Need simpler wording?"}</span>
          </button>
          <span className="text-slate-300 dark:text-zinc-700">|</span>
          <button className="text-xs font-semibold text-slate-500 hover:underline flex items-center gap-1">
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Repeat Question</span>
          </button>
        </div>
      </div>

      {/* Answer Area (Text MVP) */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/40 rounded-2xl p-6 shadow-sm space-y-4">
        <label className="block text-sm font-semibold" htmlFor="answer">
          Your Response (Text Modality — Voice Dictation will be enabled in Phase 14)
        </label>
        <textarea
          id="answer"
          rows={6}
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
          placeholder="Type your technical response here. Speak with clarity and include key concepts..."
          className="w-full p-4 border rounded-xl dark:bg-black dark:border-amber-400/50 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
        />

        <div className="flex items-center justify-between pt-2">
          <span className="text-xs opacity-60">Shortcuts: Alt+S to Submit</span>
          <div className="flex items-center gap-3">
            <Link
              to={`/report/${id}`}
              className="px-4 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-zinc-700 hover:bg-slate-100 dark:hover:bg-zinc-800"
            >
              End Interview Early
            </Link>
            <button
              onClick={() => alert("Answer submission will trigger Evaluation & Decision Policy Agent in Phase 10-12.")}
              className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl shadow flex items-center gap-2 dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300"
            >
              <span>Submit Answer</span>
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
