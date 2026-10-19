import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Database, ArrowRight, Layers } from 'lucide-react';
import AccessibilityPreview from '../components/AccessibilityPreview';

export default function HomePage() {
  const closedLoopSteps = [
    {
      step: '01',
      title: 'Interview State',
      desc: 'Tracks covered topics, difficulty levels, and responses across each turn of the interview.'
    },
    {
      step: '02',
      title: 'Decision Policy',
      desc: 'Decides whether to ask a follow-up question, adjust difficulty, change topic, or conclude.'
    },
    {
      step: '03',
      title: 'Question Formulation',
      desc: 'Formulates questions relevant to the target role and candidate background using curated topic knowledge.'
    },
    {
      step: '04',
      title: 'Response Evaluation',
      desc: 'Assesses answer content and technical depth while supporting accessible input modes.'
    },
    {
      step: '05',
      title: 'State Update',
      desc: 'Updates progress and topic mastery vectors, feeding the result back into the policy for the next question.'
    }
  ];

  const questionCategories = [
    { title: 'Python / Java / JS', count: 'Language fundamentals, async, memory models, and standard libraries' },
    { title: 'Web & REST APIs', count: 'HTTP semantics, REST conventions, API design, and authentication' },
    { title: 'SQL & DBMS', count: 'Queries, indexing, transactions, and basic database design' },
    { title: 'AI & Machine Learning', count: 'ML concepts, prompt design, embeddings, and model evaluation' },
    { title: 'Data Structures & Algorithms', count: 'Arrays, trees, basic algorithms, and complexity analysis' },
    { title: 'System Fundamentals', count: 'Concurrency, caching, networking basics, and component design' },
  ];

  return (
    <div className="space-y-28 py-12">
      {/* 1. Hero Section */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold uppercase tracking-wider"
        >
          <Sparkles className="w-4 h-4 text-indigo-600" />
          Accessible Technical Mock Interviews
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight"
        >
          Practice technical interviews with <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">
            questions that adapt to your answers
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="max-w-3xl mx-auto text-lg text-slate-600 leading-relaxed"
        >
          AccessHire AI helps you prepare for technical job interviews. The platform tailors questions to your
          resume and job description, adjusts difficulty as you practice, and includes configurable accessibility settings.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-wrap items-center justify-center gap-4 pt-2"
        >
          <a
            href="http://localhost:5174/register"
            className="inline-flex items-center gap-2 px-7 py-3.5 text-base font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-md hover:shadow-lg transition-all focus:outline-none focus:ring-4 focus:ring-indigo-300"
          >
            <span>Start Practice</span>
            <ArrowRight className="w-5 h-5" />
          </a>
          <a
            href="#accessibility-showcase"
            className="inline-flex items-center gap-2 px-7 py-3.5 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl transition-all focus:outline-none focus:ring-4 focus:ring-slate-200"
          >
            <span>See Accessibility Options</span>
          </a>
        </motion.div>
      </section>

      {/* 2. Adaptive Interview Flow */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Interview Flow</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
            How the Adaptive Interview Works
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            Instead of a fixed question list, the platform uses an adaptive decision loop that evaluates each response
            before choosing the next step.
          </p>
        </div>

        {/* Visual Workflow Steps */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {closedLoopSteps.map((item, idx) => (
            <div key={idx} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3 flex flex-col justify-between hover:border-indigo-300 transition-colors">
              <div className="space-y-2">
                <span className="text-2xl font-black text-indigo-600/30">{item.step}</span>
                <h3 className="font-bold text-slate-900 text-sm">{item.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{item.desc}</p>
              </div>
              <div className="pt-2 text-indigo-600 text-xs font-semibold flex items-center gap-1">
                <span>Next Step</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>

        {/* Dynamic Action Showcase */}
        <div className="bg-slate-900 rounded-3xl p-8 sm:p-10 text-white shadow-xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div className="space-y-4">
            <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Decision Policy</span>
            <h3 className="text-2xl font-bold">Possible Interview Actions</h3>
            <p className="text-sm text-slate-300 leading-relaxed">
              Based on candidate responses and session goals, the policy can take several actions:
            </p>
            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-emerald-300">✓ NEW_QUESTION</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-amber-300">✓ FOLLOW_UP</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-cyan-300">✓ INCREASE_DIFFICULTY</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-rose-300">✓ DECREASE_DIFFICULTY</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-indigo-300">✓ CHANGE_TOPIC</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300">✓ END_INTERVIEW</span>
            </div>
          </div>
          <div className="bg-slate-800/90 rounded-2xl p-6 border border-slate-700 space-y-3 font-mono text-xs">
            <div className="text-indigo-400 font-bold flex items-center gap-2">
              <Layers className="w-4 h-4" />
              <span>Sample Turn (Illustrative Example)</span>
            </div>
            <div className="text-slate-400">1. Current Topic: Python Concurrency [Score: 5.0 / 10]</div>
            <div className="text-amber-400 pl-4">↳ Policy: FOLLOW_UP (clarify thread safety)</div>
            <div className="text-cyan-400 pl-8">↳ Question: Focus on synchronization primitives</div>
            <div className="text-emerald-400 pl-12">↳ Candidate explains Lock and Semaphore usage</div>
            <div className="text-indigo-400 pl-16">↳ State updated: topic mastery advances ↺</div>
          </div>
        </div>
      </section>

      {/* 3. Question Topics */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Question Coverage</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
            Curated Technical Question Topics
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            Questions are drawn from curated technical topics covering common software engineering domains,
            helping keep interview practice grounded and relevant.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {questionCategories.map((cat, idx) => (
            <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-2 hover:shadow-md transition-shadow">
              <div className="flex items-center gap-2 text-indigo-600 font-bold text-base">
                <Database className="w-4 h-4" />
                <span>{cat.title}</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">{cat.count}</p>
            </div>
          ))}
        </div>

        <div className="bg-indigo-50 border border-indigo-200 rounded-2xl p-6 text-sm text-slate-700 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="space-y-1">
            <h4 className="font-bold text-slate-900">Session Variety</h4>
            <p className="text-xs text-slate-600">
              The system is designed to check past questions within the session to reduce repeats and keep practice varied.
            </p>
          </div>
          <a
            href="http://localhost:5174/setup"
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow transition-colors flex-shrink-0"
          >
            Start Practice Setup
          </a>
        </div>
      </section>

      {/* 4. Accessibility Showcase */}
      <section id="accessibility-showcase" className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Accessibility</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
            Accessibility Features
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            Try out preview settings below for high contrast, text scaling, and plain-language question wording.
          </p>
        </div>

        <AccessibilityPreview />
      </section>

      {/* 5. Bottom Call to Action */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center pb-8">
        <div className="bg-gradient-to-r from-indigo-600 to-violet-700 rounded-3xl p-10 sm:p-14 text-white shadow-2xl space-y-6">
          <h2 className="text-3xl sm:text-4xl font-extrabold">Ready to practice your technical interview?</h2>
          <p className="max-w-2xl mx-auto text-indigo-100 text-sm leading-relaxed">
            Practice with questions tailored to your target job, with accessibility settings you can adjust at any time.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <a
              href="http://localhost:5174/register"
              className="px-8 py-3.5 bg-white text-indigo-600 hover:bg-indigo-50 font-bold rounded-xl shadow-lg transition-all focus:outline-none focus:ring-4 focus:ring-white/40"
            >
              Get Started
            </a>
            <a
              href="http://localhost:5174/login"
              className="px-8 py-3.5 bg-indigo-800/80 hover:bg-indigo-800 text-white font-semibold rounded-xl border border-indigo-400/40 transition-all focus:outline-none focus:ring-4 focus:ring-indigo-400"
            >
              Sign In
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
