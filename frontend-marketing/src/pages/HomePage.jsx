import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Brain, Cpu, Volume2, ShieldCheck, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="space-y-24 py-12">
      {/* Hero Section */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold uppercase tracking-wider"
        >
          <Sparkles className="w-4 h-4 text-indigo-600" />
          Adaptive Agentic AI Mock Interview Platform
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight"
        >
          Master Job Interviews with <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">
            Adaptive, Accessible AI
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="max-w-3xl mx-auto text-lg text-slate-600 leading-relaxed"
        >
          AccessHire AI goes beyond linear chatbots. Using a research-backed closed-loop policy engine,
          the system calibrates question difficulty, delves deeper into your responses, and personalizes
          interview practice for candidates with diverse accessibility preferences.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-wrap items-center justify-center gap-4 pt-4"
        >
          <a
            href="http://localhost:5174/register"
            className="inline-flex items-center gap-2 px-6 py-3 text-base font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-md hover:shadow-lg transition-all focus:outline-none focus:ring-4 focus:ring-indigo-300"
          >
            <span>Launch Mock Interview</span>
            <ArrowRight className="w-5 h-5" />
          </a>
          <a
            href="/about"
            className="inline-flex items-center gap-2 px-6 py-3 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl transition-all focus:outline-none focus:ring-4 focus:ring-slate-200"
          >
            <span>Read Architecture</span>
          </a>
        </motion.div>
      </section>

      {/* Core Research Novelty Preview */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-900 rounded-3xl p-8 sm:p-12 text-white shadow-2xl relative overflow-hidden">
          <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Core Research Contribution</span>
              <h2 className="text-3xl font-bold text-white">Closed-Loop Adaptive Policy Engine</h2>
              <p className="text-slate-300 leading-relaxed text-sm">
                Rather than generating static scripted questions upfront, AccessHire AI continuously measures
                concept mastery and dynamically executes decisions: whether to ask targeted follow-ups,
                increase difficulty, explore missing domains, or provide accessibility accommodations.
              </p>
              <ul className="space-y-3 text-sm text-slate-300">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Topic Mastery & Difficulty Calibration Vectors</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Multi-agent LangGraph orchestration with Central Supervisor</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>Configurable accessibility accommodations (Voice, High-Contrast, Plain English)</span>
                </li>
              </ul>
            </div>
            <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 font-mono text-xs space-y-4">
              <div className="text-indigo-400 font-bold"># Live Interview State Cycle</div>
              <div className="text-slate-400">1. Interview State Engine [Topic Mastery + Depth]</div>
              <div className="text-amber-400 pl-4">↳ Decision Policy Agent [DECISION: FOLLOW_UP]</div>
              <div className="text-slate-400 pl-8">↳ Question Generator [Probe Technical Sub-topic]</div>
              <div className="text-emerald-400 pl-12">↳ Candidate Response [Voice/Text Answer]</div>
              <div className="text-cyan-400 pl-16">↳ Evaluation Agent [Rubric Multi-metric Score]</div>
              <div className="text-indigo-400 pl-20">↳ State Update & Calibration Loop ↺</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
