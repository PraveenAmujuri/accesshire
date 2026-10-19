import React from 'react';
import { GitBranch, ShieldCheck, Database, Cpu, CheckCircle2, ArrowRight } from 'lucide-react';

export default function AboutPage() {
  const agents = [
    { num: '1', name: 'Candidate & Job Analysis Agent', role: 'Consolidated extraction of candidate competencies, projects, and job requirements.' },
    { num: '2', name: 'Interview Planner Agent', role: 'Constructs initial session blueprint, topic weights, difficulty, and question distribution.' },
    { num: '3', name: 'Decision Policy Agent', role: 'Core research novelty: dynamically decides next action (follow-up, escalate/de-escalate, change topic, end).' },
    { num: '4', name: 'Question Generation Agent', role: 'Adapts curated RAG domain questions to candidate profile and accessibility settings with deduplication.' },
    { num: '5', name: 'Evaluation Agent', role: 'Multi-metric rubric assessment (relevance, depth, technical accuracy); pause-tolerant for speech variations.' },
    { num: '6', name: 'Feedback Agent', role: 'Generates understandable, actionable, and encouraging feedback after interview conclusion.' },
    { num: '7', name: 'Skill Gap & Learning Agent', role: 'Consolidated diagnostic matrix mapping deficient areas directly to a 2–4 week milestone roadmap.' },
  ];

  const pillars = [
    {
      title: 'Central Orchestrator & System Monitor',
      note: 'Not an AI Agent',
      desc: 'Controls execution order, validates Pydantic schemas, handles retries with exponential backoff, runs fallbacks, and logs telemetry.'
    },
    {
      title: 'Interview State Engine',
      note: 'State Management',
      desc: 'Maintains live topic mastery vectors, dynamic difficulty levels, previous questions, scores, and accessibility settings.'
    },
    {
      title: 'Curated RAG Question Knowledge Base',
      note: 'Knowledge Grounding',
      desc: 'Maintains curated IT/CS interview questions across foundational categories with vector retrieval and session deduplication.'
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
      {/* Intro */}
      <div className="space-y-4">
        <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Academic & Technical Architecture</span>
        <h1 className="text-4xl font-extrabold text-slate-900">Final-Year B.Tech AI & ML Project</h1>
        <p className="text-slate-600 text-base leading-relaxed">
          AccessHire AI is an Agentic AI-powered accessible mock interview platform engineered to replace static scripted interview bots
          with an <strong>Adaptive Closed-Loop Decision Engine</strong> that continuously calibrates to candidate responses.
        </p>
      </div>

      {/* Novelty Clarification */}
      <div className="bg-indigo-50 border border-indigo-200 rounded-3xl p-8 space-y-4">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-indigo-600" />
          The Core Research Contribution
        </h2>
        <p className="text-sm text-slate-700 leading-relaxed">
          The primary novelty is <strong>not</strong> simply running multiple agents. The novelty is the 
          <strong> Adaptive Closed-Loop Decision Policy</strong>. Rather than following a predetermined list of questions,
          the system maintains a structured interview state vector and runs a continuous decision cycle:
        </p>
        <div className="p-4 bg-white rounded-xl border border-indigo-100 font-mono text-xs text-indigo-900 space-y-1.5">
          <div>Interview State ➔ Decision Policy ➔ Next Action (Follow-Up / Scale Difficulty / Change Topic)</div>
          <div className="pl-6">➔ Question Generation (RAG Grounded) ➔ Candidate Answer (Voice / Text)</div>
          <div className="pl-12">➔ Accessible Evaluation ➔ State Update & Mastery Calibration ➔ (Repeat Policy) ↺</div>
        </div>
      </div>

      {/* 7 Functional Agents */}
      <div className="space-y-6">
        <div className="border-b pb-3 border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900">The 7 Functional AI Agents</h2>
          <p className="text-xs text-slate-500 mt-1">Modularly orchestrated in LangGraph without redundant agent proliferation.</p>
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

      {/* 3 Non-Agent Pillars */}
      <div className="space-y-6">
        <div className="border-b pb-3 border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900">Core System Infrastructure Pillars</h2>
          <p className="text-xs text-slate-500 mt-1">Foundational components providing resilience, state persistence, and knowledge grounding.</p>
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
          <span>Launch Interview Practice Platform</span>
          <ArrowRight className="w-4 h-4" />
        </a>
      </div>
    </div>
  );
}
