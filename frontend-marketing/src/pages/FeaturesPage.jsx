import React from 'react';
import { FileText, Sliders, Database, ShieldCheck, Award, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function FeaturesPage() {
  const coreFeatures = [
    {
      icon: <FileText className="w-6 h-6 text-indigo-600" />,
      title: "1. Candidate & Job Analysis",
      tag: "Agent 1",
      description: "Extracts key skills and experience from your resume and matches them against the target job requirements."
    },
    {
      icon: <Sliders className="w-6 h-6 text-indigo-600" />,
      title: "2. Interview Planner",
      tag: "Agent 2",
      description: "Creates an initial interview plan covering relevant topics, question distribution, and starting difficulty."
    },
    {
      icon: <Award className="w-6 h-6 text-indigo-600" />,
      title: "3. Decision Policy",
      tag: "Agent 3",
      description: "Evaluates each answer to decide the next step: ask a follow-up, adjust difficulty, switch topic, or wrap up."
    },
    {
      icon: <Database className="w-6 h-6 text-indigo-600" />,
      title: "4. Question Generation",
      tag: "Agent 4",
      description: "Formulates questions using curated technical topics, adapting them to the candidate and accessibility settings."
    },
    {
      icon: <ShieldCheck className="w-6 h-6 text-indigo-600" />,
      title: "5. Evaluation",
      tag: "Agent 5",
      description: "Assesses answer relevance, technical correctness, and depth without penalizing natural pauses or repetitions."
    },
    {
      icon: <FileText className="w-6 h-6 text-indigo-600" />,
      title: "6. Feedback",
      tag: "Agent 6",
      description: "Summarizes interview performance with clear strengths and practical areas to review."
    },
    {
      icon: <Award className="w-6 h-6 text-indigo-600" />,
      title: "7. Skill Gap & Learning Roadmap",
      tag: "Agent 7",
      description: "Identifies areas that need improvement and suggests structured topics for post-interview preparation."
    },
  ];

  const a11yFeatures = [
    {
      title: "Intellectual Disabilities Accommodations",
      desc: "Optional plain-language question wording, step-by-step conceptual breakdowns, and untimed deliberation."
    },
    {
      title: "Autism Spectrum (ASD) Accommodations",
      desc: "Direct and unambiguous questions, visible topic progress, and a low-distraction visual layout."
    },
    {
      title: "Deaf / Hard of Hearing Accommodations",
      desc: "Text display for all spoken questions, captions, and visual status indicators for recording and evaluation."
    },
    {
      title: "Speech Disabilities Accommodations",
      desc: "Choice of voice or typed text responses, with pause-tolerant input and evaluation focused on technical content."
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-20">
      {/* Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <span className="text-xs uppercase font-bold tracking-widest text-indigo-600">Platform Overview</span>
        <h1 className="text-4xl font-extrabold text-slate-900">Platform Features</h1>
        <p className="text-slate-600 text-base leading-relaxed">
          How AccessHire AI structures mock interviews, from initial setup to feedback.
        </p>
      </div>

      {/* 7 Functional Agents Grid */}
      <div className="space-y-6">
        <div className="flex items-center justify-between border-b pb-3 border-slate-200">
          <h2 className="text-2xl font-bold text-slate-900">Seven-Agent Architecture</h2>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-indigo-100 text-indigo-700">
            Structured Workflow
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {coreFeatures.map((f, idx) => (
            <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow space-y-3 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center">
                    {f.icon}
                  </div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                    {f.tag}
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900">{f.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{f.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Accessibility Accommodations Breakdown */}
      <div className="bg-slate-900 text-white rounded-3xl p-8 sm:p-12 space-y-8 shadow-xl">
        <div className="max-w-2xl space-y-2">
          <span className="text-xs uppercase font-bold tracking-widest text-indigo-400">Accessibility</span>
          <h2 className="text-3xl font-bold">Supported Accessibility Accommodations</h2>
          <p className="text-sm text-slate-300">
            Settings designed to assist candidates with common cognitive, sensory, and communication needs:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {a11yFeatures.map((a, i) => (
            <div key={i} className="p-5 rounded-2xl bg-slate-800 border border-slate-700 space-y-2">
              <h4 className="font-bold text-indigo-300 text-sm flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                {a.title}
              </h4>
              <p className="text-xs text-slate-300 leading-relaxed">{a.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Call to Action Bar */}
      <div className="p-8 bg-indigo-50 border border-indigo-200 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-1">
          <h3 className="text-xl font-bold text-slate-900">Start Your Interview Practice</h3>
          <p className="text-xs text-slate-600">Configure your target role and accessibility settings in the interview platform.</p>
        </div>
        <div className="flex items-center gap-3">
          <a
            href="http://localhost:5174/login"
            className="px-5 py-2.5 text-xs font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 rounded-xl transition-colors"
          >
            Sign In
          </a>
          <a
            href="http://localhost:5174/register"
            className="px-5 py-2.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow transition-colors flex items-center gap-1.5"
          >
            <span>Start Practice</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
}
