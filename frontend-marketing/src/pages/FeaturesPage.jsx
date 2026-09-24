import React from 'react';
import { FileText, Briefcase, Sliders, Volume2, ShieldAlert, Award } from 'lucide-react';

export default function FeaturesPage() {
  const features = [
    {
      icon: <FileText className="w-6 h-6 text-indigo-600" />,
      title: "Resume Intelligence",
      description: "Extracts technical competencies, project depth, and experience years using structured document processing."
    },
    {
      icon: <Briefcase className="w-6 h-6 text-indigo-600" />,
      title: "Job Criteria Alignment",
      description: "Analyzes target Job Descriptions, identifying primary evaluation rubrics and seniority expectations."
    },
    {
      icon: <Sliders className="w-6 h-6 text-indigo-600" />,
      title: "Adaptive Decision Policy",
      description: "Dynamic state-driven policy decides in real time whether to probe deeper, raise difficulty, or pivot topics."
    },
    {
      icon: <Volume2 className="w-6 h-6 text-indigo-600" />,
      title: "Accessibility Accommodations",
      description: "Configurable voice and text modalities, high-contrast themes, scalable typography, and simplified question phrasing."
    },
    {
      icon: <ShieldAlert className="w-6 h-6 text-indigo-600" />,
      title: "Diagnostic Skill Gap Matrix",
      description: "Pinpoints exactly where your answers fell short relative to target industry job expectations."
    },
    {
      icon: <Award className="w-6 h-6 text-indigo-600" />,
      title: "Personalized Learning Roadmap",
      description: "Transforms identified weaknesses into an actionable 2 to 4 week milestone-based study curriculum."
    },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12">
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <h1 className="text-4xl font-extrabold text-slate-900">Platform Features</h1>
        <p className="text-slate-600 text-lg">
          An end-to-end agentic workflow engineered for realistic, accessible mock interview preparation.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map((f, idx) => (
          <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow space-y-3">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center">
              {f.icon}
            </div>
            <h2 className="text-lg font-bold text-slate-900">{f.title}</h2>
            <p className="text-sm text-slate-600 leading-relaxed">{f.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
