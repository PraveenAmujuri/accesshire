import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Brain, Database, Sliders, CheckCircle2, ArrowRight, ShieldCheck, RefreshCw, Layers } from 'lucide-react';
import AccessibilityPreview from '../components/AccessibilityPreview';

export default function HomePage() {
  const closedLoopSteps = [
    {
      step: '01',
      title: 'Interview State Engine',
      desc: 'Tracks topic mastery vectors, difficulty levels, answer trajectory, and accessibility accommodations across every turn.'
    },
    {
      step: '02',
      title: 'Decision Policy Agent',
      desc: 'Evaluates state history and decides: ask follow-up, raise/lower difficulty, switch topic, clarify, or end interview.'
    },
    {
      step: '03',
      title: 'Question Generation + RAG',
      desc: 'Retrieves relevant domain questions from curated IT/CS knowledge base and adapts them dynamically to the candidate.'
    },
    {
      step: '04',
      title: 'Multi-Metric Evaluation',
      desc: 'Evaluates semantic depth and technical correctness without penalizing natural speech pauses or dysarthria.'
    },
    {
      step: '05',
      title: 'State Update & Calibration',
      desc: 'Calibrates topic competency scores and feeds the updated state back to the policy agent for the next turn.'
    }
  ];

  const ragCategories = [
    { title: 'Python / Java / JS', count: 'Core language internals, async, GIL, memory models' },
    { title: 'Web & REST APIs', count: 'FastAPI, Express, HTTP semantics, auth & rate limiting' },
    { title: 'SQL & DBMS', count: 'Indexing, ACID transactions, normalization, query planning' },
    { title: 'AI & Machine Learning', count: 'Prompt engineering, embeddings, RAG evaluation, metrics' },
    { title: 'DSA & Algorithms', count: 'Tree traversals, dynamic programming, time/space trade-offs' },
    { title: 'System Architecture', count: 'Microservices, caching, message queues, reliability' },
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
          Adaptive Agentic AI Mock Interview Platform
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight"
        >
          Master Technical Interviews with <br />
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
          AccessHire AI is not a generic scripted chatbot. Built with a closed-loop decision policy and
          a curated RAG question knowledge base, it dynamically adjusts question difficulty, probes your
          technical depth, and provides tailored accommodations for candidates with diverse accessibility needs.
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
            <span>Start Mock Practice</span>
            <ArrowRight className="w-5 h-5" />
          </a>
          <a
            href="#accessibility-showcase"
            className="inline-flex items-center gap-2 px-7 py-3.5 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl transition-all focus:outline-none focus:ring-4 focus:ring-slate-200"
          >
            <span>Explore Accessibility Tools</span>
          </a>
        </motion.div>
      </section>

      {/* 2. Research Novelty: Closed-Loop Decision Engine */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Core Research Contribution</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
            Adaptive Closed-Loop Interview Orchestration
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            The novelty of AccessHire AI is not merely using multiple AI agents. It lies in maintaining a live
            interview state matrix that drives policy-based decisions at every turn of the interview.
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
                <span>Next Loop</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>

        {/* Dynamic Action Showcase */}
        <div className="bg-slate-900 rounded-3xl p-8 sm:p-10 text-white shadow-xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div className="space-y-4">
            <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Policy Actions</span>
            <h3 className="text-2xl font-bold">What the Decision Policy Agent Decides:</h3>
            <p className="text-sm text-slate-300 leading-relaxed">
              Based on candidate mastery and past turn rubrics, the policy dynamically chooses the optimal pedagogical step:
            </p>
            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-emerald-300">✓ NEW_QUESTION</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-amber-300">✓ FOLLOW_UP (Probe)</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-cyan-300">✓ INCREASE_DIFFICULTY</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-rose-300">✓ DECREASE_DIFFICULTY</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-indigo-300">✓ CHANGE_TOPIC</span>
              <span className="p-2.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300">✓ END_INTERVIEW</span>
            </div>
          </div>
          <div className="bg-slate-800/90 rounded-2xl p-6 border border-slate-700 space-y-3 font-mono text-xs">
            <div className="text-indigo-400 font-bold flex items-center gap-2">
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Live Closed-Loop Trajectory Trace</span>
            </div>
            <div className="text-slate-400">1. State: Python Concurrency [Score: 4.8 / 10]</div>
            <div className="text-amber-400 pl-4">↳ Policy: DECREASE_DIFFICULTY + CLARIFICATION</div>
            <div className="text-cyan-400 pl-8">↳ RAG Knowledge: Python Threading Baselines</div>
            <div className="text-emerald-400 pl-12">↳ Candidate explains thread concept with clarity</div>
            <div className="text-indigo-400 pl-16">↳ Evaluator updates mastery vector to 7.8 / 10 ↺</div>
          </div>
        </div>
      </section>

      {/* 3. Supporting Novelty: Curated RAG Question Knowledge Base */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Knowledge Grounding</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
            Curated RAG Question Knowledge Base
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            The platform does not rely entirely on unconstrained LLM hallucinations. It grounds question generation
            in a curated, metadata-filtered IT/CS question knowledge base covering foundational disciplines.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ragCategories.map((cat, idx) => (
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
            <h4 className="font-bold text-slate-900">RAG Question Deduplication & Context Adaptation</h4>
            <p className="text-xs text-slate-600">
              The Question Generation Agent checks previously asked question signatures within the session so candidates never receive duplicate questions.
            </p>
          </div>
          <a
            href="http://localhost:5174/setup"
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow transition-colors flex-shrink-0"
          >
            Configure Session Blueprint
          </a>
        </div>
      </section>

      {/* 4. Interactive Accessibility Showcase */}
      <section id="accessibility-showcase" className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Inclusive Design</span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
            Interactive Accessibility Showcase
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            Experience our configurable accommodation features directly below. Toggle high-contrast, adjust typography,
            and preview plain-language question alternatives.
          </p>
        </div>

        <AccessibilityPreview />
      </section>

      {/* 5. Bottom Call to Action */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center pb-8">
        <div className="bg-gradient-to-r from-indigo-600 to-violet-700 rounded-3xl p-10 sm:p-14 text-white shadow-2xl space-y-6">
          <h2 className="text-3xl sm:text-4xl font-extrabold">Ready to Practice Your Next Interview?</h2>
          <p className="max-w-2xl mx-auto text-indigo-100 text-sm leading-relaxed">
            Experience personalized mock interviews calibrated to your resume, target job description,
            and personal accessibility requirements.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <a
              href="http://localhost:5174/register"
              className="px-8 py-3.5 bg-white text-indigo-600 hover:bg-indigo-50 font-bold rounded-xl shadow-lg transition-all focus:outline-none focus:ring-4 focus:ring-white/40"
            >
              Get Started for Free
            </a>
            <a
              href="http://localhost:5174/login"
              className="px-8 py-3.5 bg-indigo-800/80 hover:bg-indigo-800 text-white font-semibold rounded-xl border border-indigo-400/40 transition-all focus:outline-none focus:ring-4 focus:ring-indigo-400"
            >
              Sign In to Dashboard
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
