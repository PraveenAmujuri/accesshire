import React from 'react';
import { GitBranch, Cpu, ShieldCheck } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12">
      <div className="space-y-4">
        <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Research & Architecture</span>
        <h1 className="text-4xl font-extrabold text-slate-900">Final-Year B.Tech AI & ML Project</h1>
        <p className="text-slate-600 text-base leading-relaxed">
          AccessHire AI explores the intersection of <strong>Agentic State-Graph Orchestration</strong>, <strong>Adaptive Decision Policies</strong>,
          and <strong>Cognitive Accessibility in Job Interview Preparation</strong>.
        </p>
      </div>

      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <GitBranch className="w-6 h-6 text-indigo-600" />
          The Multi-Agent Orchestration Topology
        </h2>
        <p className="text-sm text-slate-600 leading-relaxed">
          Instead of relying on a monolithic prompt or uncontrolled agent chatting, AccessHire AI utilizes
          a structured LangGraph state machine with a centralized Orchestrator/Supervisor:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">1. Resume Analysis Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">2. Job Analysis Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">3. Interview Planner Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">4. Decision Policy Agent (Core)</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">5. Question Generation Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">6. Multi-Metric Evaluation Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">7. Constructive Feedback Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">8. Skill Gap Diagnostic Agent</div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">9. Learning Roadmap Agent</div>
          <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-lg text-indigo-700 font-bold">10. Central Orchestrator / Supervisor</div>
        </div>
      </div>
    </div>
  );
}
