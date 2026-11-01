import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Upload,
  Briefcase,
  Sliders,
  Play,
  AlertCircle,
  Loader2,
  CheckCircle2,
  FileText,
  Sparkles,
  X,
  Target,
  Layers,
  ArrowRight
} from 'lucide-react';
import { interviewApi } from '../api/interviewApi';

export default function SetupPage() {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  // Job & session state
  const [jobTitle, setJobTitle] = useState('Python Backend Developer');
  const [jobDescription, setJobDescription] = useState('Developing scalable REST APIs using FastAPI, async/await, and database integration.');
  const [targetQuestionCount, setTargetQuestionCount] = useState(3);
  const [simplifiedLanguage, setSimplifiedLanguage] = useState(false);
  const [extendedTime, setExtendedTime] = useState(true);

  // Resume upload state
  const [resumeFile, setResumeFile] = useState(null);
  const [uploadedResume, setUploadedResume] = useState(null);
  const [uploadingResume, setUploadingResume] = useState(false);

  // Agent 1: Candidate & Job Analysis state
  const [analyzingProfile, setAnalyzingProfile] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  // General submission & error state
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Handle file selection
  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext !== 'pdf' && ext !== 'docx') {
      setErrorMessage('Please select a valid PDF (.pdf) or Word document (.docx).');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setErrorMessage('Resume file size exceeds the 10MB limit.');
      return;
    }

    setResumeFile(file);
    setUploadingResume(true);
    setErrorMessage('');
    setAnalysisResult(null);

    try {
      const res = await interviewApi.uploadResume(file);
      setUploadedResume(res);
    } catch (err) {
      setErrorMessage(err.message || 'Failed to upload and parse resume file.');
      setResumeFile(null);
      setUploadedResume(null);
    } finally {
      setUploadingResume(false);
    }
  };

  const handleRemoveResume = () => {
    setResumeFile(null);
    setUploadedResume(null);
    setAnalysisResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Run Agent 1: Candidate & Job Analysis
  const handleRunAnalysis = async () => {
    if (!jobDescription.trim()) {
      setErrorMessage('Please enter a job description before running analysis.');
      return;
    }

    setAnalyzingProfile(true);
    setErrorMessage('');

    try {
      const res = await interviewApi.analyzeCandidateJob({
        resume_id: uploadedResume?.resume_id,
        job_title: jobTitle.trim(),
        job_description: jobDescription.trim(),
      });

      if (res && res.analysis) {
        setAnalysisResult(res.analysis);
      }
    } catch (err) {
      setErrorMessage(err.message || 'Candidate & Job Analysis failed.');
    } finally {
      setAnalyzingProfile(false);
    }
  };

  const handleStartInterview = async (e) => {
    e.preventDefault();
    if (!jobTitle.trim()) {
      setErrorMessage('Please provide a job title or target role.');
      return;
    }

    setLoading(true);
    setErrorMessage('');

    try {
      const session = await interviewApi.startSession({
        job_title: jobTitle.trim(),
        job_description: jobDescription.trim(),
        resume_id: uploadedResume?.resume_id || null,
        target_question_count: Number(targetQuestionCount) || 3,
        simplified_language: simplifiedLanguage,
        extended_time: extendedTime,
        voice_enabled: false,
      });

      if (session && session.session_id) {
        navigate(`/interview/${session.session_id}`);
      } else {
        throw new Error('Session creation did not return a valid session ID.');
      }
    } catch (err) {
      setErrorMessage(err.message || 'Failed to initialize interview session.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold">Configure Interview Session</h1>
        <p className="text-sm opacity-70">
          Upload your resume, specify your target job requirements, and personalize your accessibility settings
        </p>
      </div>

      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-2.5">
          <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-600 mt-0.5" />
          <div>
            <strong className="block font-semibold">Error</strong>
            <span>{errorMessage}</span>
          </div>
        </div>
      )}

      <form onSubmit={handleStartInterview} className="space-y-8">
        {/* 1. Job Description & Role */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Briefcase className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>1. Target Job Role & Description</span>
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="jobTitle">Job Title / Target Role</label>
            <input
              id="jobTitle"
              type="text"
              required
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="e.g. Python Backend Developer"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="jd">Job Description / Requirements</label>
            <textarea
              id="jd"
              rows={4}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm font-mono focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="Paste job description requirements, technical stack, and responsibilities..."
            />
          </div>
          <div className="pt-1">
            <label className="block text-xs font-semibold uppercase mb-1" htmlFor="count">Number of Questions</label>
            <select
              id="count"
              value={targetQuestionCount}
              onChange={(e) => setTargetQuestionCount(Number(e.target.value))}
              className="px-3 py-2 border rounded-lg dark:bg-black dark:border-amber-400/40 text-sm focus:ring-2 focus:ring-indigo-500 outline-none"
            >
              <option value={2}>2 Questions (Quick Practice)</option>
              <option value={3}>3 Questions (Standard)</option>
              <option value={5}>5 Questions (In-depth)</option>
            </select>
          </div>
        </div>

        {/* 2. Candidate Resume Upload (PDF / DOCX) */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 font-bold text-lg">
              <Upload className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
              <span>2. Candidate Resume (PDF / DOCX)</span>
            </div>
            {uploadedResume && (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                <CheckCircle2 className="w-3.5 h-3.5" />
                Parsed & Ready
              </span>
            )}
          </div>

          <p className="text-xs opacity-70">
            Upload your resume so the Candidate & Job Analysis Agent can extract your technical competencies, detect experience levels, and calibrate interview questions to your background.
          </p>

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            className="hidden"
          />

          {!uploadedResume && !uploadingResume && (
            <div
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-slate-300 dark:border-zinc-700 hover:border-indigo-500 dark:hover:border-amber-400 rounded-xl p-8 text-center cursor-pointer transition-colors bg-slate-50/50 dark:bg-black/20"
            >
              <FileText className="w-10 h-10 mx-auto text-slate-400 dark:text-zinc-600 mb-2" />
              <div className="font-semibold text-sm">Click to upload your resume</div>
              <div className="text-xs opacity-60 mt-1">Supports PDF (.pdf) and Microsoft Word (.docx) up to 10MB</div>
            </div>
          )}

          {uploadingResume && (
            <div className="border border-slate-200 dark:border-zinc-800 rounded-xl p-6 text-center bg-slate-50 dark:bg-zinc-900/50 flex flex-col items-center justify-center gap-2">
              <Loader2 className="w-8 h-8 animate-spin text-indigo-600 dark:text-amber-400" />
              <div className="text-sm font-semibold">Extracting resume text with PyMuPDF/docx...</div>
            </div>
          )}

          {uploadedResume && (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3.5 rounded-xl border border-slate-200 dark:border-zinc-800 bg-slate-50 dark:bg-black/40">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-indigo-50 dark:bg-amber-400/10 text-indigo-600 dark:text-amber-400">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-sm font-bold">{uploadedResume.filename}</div>
                    <div className="text-xs opacity-60">
                      {(uploadedResume.file_size / 1024).toFixed(1)} KB • {uploadedResume.char_count} characters extracted
                    </div>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={handleRemoveResume}
                  className="p-1.5 rounded-lg hover:bg-slate-200 dark:hover:bg-zinc-800 text-slate-500 transition-colors"
                  title="Remove resume"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Agent 1 Analysis Trigger */}
              <div className="flex items-center justify-between pt-1">
                <button
                  type="button"
                  onClick={handleRunAnalysis}
                  disabled={analyzingProfile}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold border border-indigo-200 dark:border-amber-400/40 bg-indigo-50/70 dark:bg-amber-400/10 text-indigo-700 dark:text-amber-400 hover:bg-indigo-100 dark:hover:bg-amber-400/20 transition-all shadow-sm"
                >
                  {analyzingProfile ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Analyzing Profile with Agent 1...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      <span>Analyze Profile & Match Job (Agent 1)</span>
                    </>
                  )}
                </button>
                <span className="text-xs opacity-60">Optional preview before starting</span>
              </div>

              {/* Agent 1 Analysis Results Card */}
              {analysisResult && (
                <div className="p-5 rounded-xl border border-indigo-200 dark:border-amber-400/40 bg-gradient-to-br from-indigo-50/40 to-white dark:from-zinc-900 dark:to-black space-y-4 text-xs">
                  <div className="flex items-center justify-between border-b border-indigo-100 dark:border-zinc-800 pb-3">
                    <div className="flex items-center gap-2 font-bold text-sm text-indigo-950 dark:text-amber-300">
                      <Target className="w-4 h-4" />
                      <span>Agent 1 Profile & Match Analysis</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded-full bg-indigo-100 dark:bg-amber-400/20 font-semibold text-indigo-800 dark:text-amber-300 uppercase tracking-wider text-[10px]">
                        {analysisResult.experience_level} Level
                      </span>
                      <span className="px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 font-bold">
                        {analysisResult.skill_match_analysis?.match_score}% Match
                      </span>
                    </div>
                  </div>

                  <div>
                    <span className="font-semibold block text-slate-700 dark:text-zinc-300 mb-1">Candidate Summary:</span>
                    <p className="opacity-80 leading-relaxed">{analysisResult.candidate_summary}</p>
                  </div>

                  {/* Skills Grid */}
                  <div className="space-y-1.5">
                    <span className="font-semibold block text-slate-700 dark:text-zinc-300">Extracted Skills:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {analysisResult.skills?.slice(0, 10).map((skill, idx) => (
                        <span key={idx} className="px-2 py-0.5 rounded-md bg-white dark:bg-zinc-800 border border-slate-200 dark:border-zinc-700 text-[11px]">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Matching vs Gap Skills */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                    <div className="p-3 rounded-lg bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/40">
                      <span className="font-semibold text-emerald-900 dark:text-emerald-400 block mb-1">Matching Requirements:</span>
                      <div className="flex flex-wrap gap-1">
                        {analysisResult.skill_match_analysis?.matching_skills?.length > 0 ? (
                          analysisResult.skill_match_analysis.matching_skills.map((s, idx) => (
                            <span key={idx} className="px-1.5 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 text-[10px]">
                              ✓ {s}
                            </span>
                          ))
                        ) : (
                          <span className="opacity-60 text-[10px]">General CS fundamentals</span>
                        )}
                      </div>
                    </div>

                    <div className="p-3 rounded-lg bg-amber-50/60 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40">
                      <span className="font-semibold text-amber-900 dark:text-amber-400 block mb-1">Identified Focus Gaps:</span>
                      <div className="flex flex-wrap gap-1">
                        {analysisResult.skill_match_analysis?.missing_or_gap_skills?.length > 0 ? (
                          analysisResult.skill_match_analysis.missing_or_gap_skills.map((s, idx) => (
                            <span key={idx} className="px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 text-[10px]">
                              • {s}
                            </span>
                          ))
                        ) : (
                          <span className="opacity-60 text-[10px]">No critical gaps identified</span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Recommended Focus Areas */}
                  {analysisResult.recommended_focus_areas?.length > 0 && (
                    <div className="space-y-1 pt-1">
                      <span className="font-semibold text-slate-700 dark:text-zinc-300 block">Recommended Interview Focus Areas:</span>
                      <ul className="list-disc list-inside space-y-0.5 opacity-80 text-[11px]">
                        {analysisResult.recommended_focus_areas.map((area, idx) => (
                          <li key={idx}>{area}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* 3. Accessibility Settings */}
        <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/30 rounded-2xl p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Sliders className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
            <span>3. Accessibility Settings</span>
          </div>
          <div className="space-y-3">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={simplifiedLanguage}
                onChange={(e) => setSimplifiedLanguage(e.target.checked)}
                className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
              />
              <div>
                <div className="text-sm font-semibold">Simplified Question Phrasing</div>
                <div className="text-xs opacity-70">Provides plain-language question alternatives without lowering technical rigor</div>
              </div>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={extendedTime}
                onChange={(e) => setExtendedTime(e.target.checked)}
                className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
              />
              <div>
                <div className="text-sm font-semibold">Extended / Untimed Response Mode</div>
                <div className="text-xs opacity-70">Disables strict countdown timers to support thoughtful deliberation</div>
              </div>
            </label>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3.5 px-6 font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 ${
            loading
              ? 'bg-indigo-400 cursor-not-allowed text-white'
              : 'bg-indigo-600 hover:bg-indigo-700 text-white dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Initializing Mock Interview...</span>
            </>
          ) : (
            <>
              <Play className="w-5 h-5" />
              <span>Start Mock Interview</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </>
          )}
        </button>
      </form>
    </div>
  );
}
