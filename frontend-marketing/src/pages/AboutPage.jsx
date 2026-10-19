import React from 'react';
import { GitBranch, ArrowRight } from 'lucide-react';

export default function AboutPage() {
  const agents = [
    { num: '1', name: 'Candidate & Job Analysis Agent', role: 'Extracts candidate skills and experience from resumes, matching them against job requirements.' },
    { num: '2', name: 'Interview Planner Agent', role: 'Builds an initial interview blueprint with topics, weights, starting difficulty, and question quotas.' },
    { num: '3', name: 'Decision Policy Agent', role: 'Decides the next interview action (ask follow-up, change difficulty, switch topic, or wrap up) after each answer.' },
    { num: '4', name: 'Question Generation Agent', role: 'Generates questions grounded in curated technical topics, adapting them to the candidate and accessibility settings.' },
    { num: '5', name: 'Evaluation Agent', role: 'Evaluates answers for technical correctness and depth, designed to accommodate speech pauses and variations.' },
    { num: '6', name: 'Feedback Agent', role: 'Summarizes interview performance with clear strengths and actionable areas for improvement.' },
    { num: '7', name: 'Skill Gap & Learning Agent', role: 'Identifies specific skill gaps and outlines a practical study roadmap for preparation.' },
  ];

  const pillars = [
    {
      title: 'Central Orchestrator',
      note: 'Workflow Control',
      desc: 'Coordinates agent execution, validates data models, handles retries, and maintains execution logs.'
    },
    {
      title: 'Interview State Engine',
      note: 'State Management',
      desc: 'Maintains topic progress, current difficulty, question history, and accessibility settings throughout the session.'
    },
    {
      title: 'Curated Question Knowledge Base',
      note: 'Topic Grounding',
      desc: 'Contains curated technical interview questions across common categories with vector search and session deduplication.'
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
      {/* Intro */}
      <div className="space-y-4">
        <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Technical Overview</span>
        <h1 className="text-4xl font-extrabold text-slate-900">System Architecture</h1>
        <p className="text-slate-600 text-base leading-relaxed">
          AccessHire AI is designed around an adaptive interview loop that adjusts questions to candidate performance
          while supporting configurable accessibility settings.
        </p>
      </div>

      {/* Decision Loop */}
      <div className="bg-indigo-50 border border-indigo-200 rounded-3xl p-8 space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-indigo-600" />
          The Adaptive Decision Loop
        </h2>
        <p className="text-sm text-slate-700 leading-relaxed">
          Rather than following a fixed script, the system maintains interview state and evaluates answers turn by turn:
        </p>
        <div className="p-4 bg-white rounded-xl border border-indigo-100 font-mono text-xs text-indigo-900 space-y-1.5">
          <div>Interview State ➔ Decision Policy ➔ Next Action (Follow-Up / Scale Difficulty / Change Topic)</div>
          <div className="pl-6">➔ Question Generation (Topic Knowledge) ➔ Candidate Answer (Voice / Text)</div>
          <div className="pl-12">➔ Evaluation ➔ State Update ➔ Next Turn Decision ↺</div>
        </div>
      </div>

      {/* 7 Functional Agents */}
      <div className="space-y-6">
        <div className="border-b pb-3 border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900">Seven Functional AI Agents</h2>
          <p className="text-xs text-slate-500 mt-1">Modular agent components coordinated through LangGraph.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((ag) => (
            <div key={ag.num} className="p-5 bg-white rounded-2xl border border-slate-200 shadow-sm space-y-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
                  {ag.num}
                </span>
                <h3 className="font-bold text-sm text-slate-900">{ag.name}</h3>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed pl-8">{ag.role}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 3 Supporting Pillars */}
      <div className="space-y-6">
        <div className="border-b pb-3 border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900">Supporting System Components</h2>
          <p className="text-xs text-slate-500 mt-1">Core infrastructure providing orchestration, state persistence, and question retrieval.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {pillars.map((pil, idx) => (
            <div key={idx} className="p-6 bg-slate-900 text-white rounded-2xl border border-slate-800 space-y-2.5">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 bg-slate-800 px-2 py-0.5 rounded">
                {pil.note}
              </span>
              <h3 className="font-bold text-sm text-white">{pil.title}</h3>
              <p className="text-xs text-slate-300 leading-relaxed">{pil.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Call to action */}
      <div className="text-center pt-6">
        <a
          href="http://localhost:5174/register"
          className="inline-flex items-center gap-2 px-8 py-3.5 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-md transition-all"
        >
          <span>Open Interview Platform</span>
          <ArrowRight className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}
