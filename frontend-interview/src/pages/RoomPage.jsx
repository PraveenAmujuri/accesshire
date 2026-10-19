import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Send, RotateCcw, Volume2, HelpCircle, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { interviewApi } from '../api/interviewApi';

export default function RoomPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answerText, setAnswerText] = useState('');
  const [simplifiedView, setSimplifiedView] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successNotice, setSuccessNotice] = useState('');

  // Fetch current question and session details
  const loadActiveQuestion = async () => {
    setLoading(true);
    setErrorMessage('');
    try {
      const [sessionData, questionData] = await Promise.all([
        interviewApi.getSession(id),
        interviewApi.getCurrentQuestion(id),
      ]);

      setSession(sessionData);
      setCurrentQuestion(questionData);

      // Default to simplified view if candidate selected simplified language in setup
      if (sessionData?.accessibility_settings?.simplified_language) {
        setSimplifiedView(true);
      }
    } catch (err) {
      // If session is already completed, redirect to report
      if (err.message && err.message.includes('completed')) {
        navigate(`/report/${id}`);
        return;
      }
      setErrorMessage(err.message || 'Failed to load the active question.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (id) {
      loadActiveQuestion();
    }
  }, [id]);

  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    if (!answerText.trim()) {
      setErrorMessage('Please type a response before submitting.');
      return;
    }

    if (!currentQuestion) return;

    setSubmitting(true);
    setErrorMessage('');
    setSuccessNotice('');

    try {
      const res = await interviewApi.submitAnswer(id, {
        question_id: currentQuestion.question_id,
        answer_text: answerText.trim(),
        modality: 'text',
      });

      if (res.is_completed) {
        // Session complete -> navigate to report
        navigate(`/report/${id}`);
      } else if (res.next_question) {
        // Advanced to next turn
        setCurrentQuestion(res.next_question);
        setAnswerText('');
        setSuccessNotice('Answer recorded. Proceeding to next question.');
        setTimeout(() => setSuccessNotice(''), 3000);
      } else {
        // Fallback: reload question state
        await loadActiveQuestion();
      }
    } catch (err) {
      setErrorMessage(err.message || 'Failed to submit answer.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleEndEarly = async () => {
    if (window.confirm('Are you sure you want to end this interview session early?')) {
      try {
        await interviewApi.endSession(id);
        navigate(`/report/${id}`);
      } catch (err) {
        setErrorMessage(err.message || 'Failed to end session.');
      }
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-indigo-600 dark:text-amber-400" />
        <p className="text-sm opacity-70">Loading active interview question...</p>
      </div>
    );
  }

  if (errorMessage && !currentQuestion) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 space-y-4 text-center">
        <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-rose-800 space-y-3">
          <AlertCircle className="w-8 h-8 text-rose-600 mx-auto" />
          <h2 className="text-lg font-bold">Session Notice</h2>
          <p className="text-sm">{errorMessage}</p>
          <div className="pt-2 flex justify-center gap-3">
            <Link
              to="/dashboard"
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-white border border-slate-300 text-slate-700 hover:bg-slate-50"
            >
              Return to Dashboard
            </Link>
            <button
              onClick={loadActiveQuestion}
              className="px-4 py-2 text-xs font-semibold rounded-lg bg-rose-600 text-white hover:bg-rose-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  const turnIndex = currentQuestion?.turn_index || 1;
  const totalTurns = currentQuestion?.total_turns || 3;
  const isLastQuestion = currentQuestion?.is_last_question || false;

  const displayQuestion = simplifiedView && currentQuestion?.simplified_question_text
    ? currentQuestion.simplified_question_text
    : currentQuestion?.question_text;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top status bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b pb-4 border-slate-200 dark:border-amber-400/30 gap-2">
        <div>
          <span className="text-xs uppercase font-bold tracking-wider text-indigo-600 dark:text-amber-400">
            Question {turnIndex} of {totalTurns}
          </span>
          <h2 className="text-lg font-bold">Topic: {currentQuestion?.topic_name || 'Technical Competency'}</h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 capitalize">
            Difficulty: {currentQuestion?.difficulty || 'Medium'}
          </span>
          {session?.accessibility_settings?.extended_time && (
            <span className="px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-100 text-slate-700 dark:bg-zinc-800 dark:text-zinc-300">
              Untimed Mode
            </span>
          )}
        </div>
      </div>

      {/* Notifications */}
      {errorMessage && (
        <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-600" />
          <span>{errorMessage}</span>
        </div>
      )}

      {successNotice && (
        <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
          <CheckCircle className="w-4 h-4 flex-shrink-0 text-emerald-600" />
          <span>{successNotice}</span>
        </div>
      )}

      {/* Question Card */}
      <div className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/40 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-start justify-between gap-4">
          <h1 className="text-xl font-bold leading-relaxed">
            {displayQuestion}
          </h1>
          <button
            title="Spoken audio read-aloud will be enabled in Phase 14"
            onClick={() => alert("Spoken question read-aloud via Web Speech API will be activated in Phase 14.")}
            className="p-2.5 rounded-xl border border-slate-200 dark:border-amber-400 hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors flex-shrink-0"
          >
            <Volume2 className="w-5 h-5 text-indigo-600 dark:text-amber-400" />
          </button>
        </div>

        <div className="flex items-center gap-3 pt-2">
          {currentQuestion?.simplified_question_text && (
            <>
              <button
                onClick={() => setSimplifiedView(prev => !prev)}
                className="text-xs font-semibold text-indigo-600 dark:text-amber-400 hover:underline flex items-center gap-1"
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>{simplifiedView ? 'Show standard phrasing' : 'Need plain-language wording?'}</span>
              </button>
              <span className="text-slate-300 dark:text-zinc-700">|</span>
            </>
          )}
          <button
            onClick={() => {
              setAnswerText('');
              setErrorMessage('');
            }}
            className="text-xs font-semibold text-slate-500 hover:underline flex items-center gap-1"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Clear Answer Draft</span>
          </button>
        </div>
      </div>

      {/* Answer Area (Text Modality) */}
      <form onSubmit={handleSubmitAnswer} className="bg-white dark:bg-zinc-900 border border-slate-200 dark:border-amber-400/40 rounded-2xl p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <label className="block text-sm font-semibold" htmlFor="answerInput">
            Your Technical Response (Text Input)
          </label>
          <span className="text-xs opacity-60">
            {answerText.trim() ? `${answerText.trim().split(/\s+/).length} words` : '0 words'}
          </span>
        </div>

        <textarea
          id="answerInput"
          rows={7}
          required
          disabled={submitting}
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
          placeholder="Explain your technical reasoning clearly, mentioning specific concepts and design trade-offs..."
          className="w-full p-4 border rounded-xl dark:bg-black dark:border-amber-400/50 text-sm focus:ring-2 focus:ring-indigo-500 outline-none font-sans leading-relaxed"
        />

        <div className="flex flex-col sm:flex-row sm:items-center justify-between pt-2 gap-3">
          <span className="text-xs opacity-60">
            {isLastQuestion ? 'Final question of this session' : `Turn ${turnIndex} of ${totalTurns}`}
          </span>
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleEndEarly}
              disabled={submitting}
              className="px-4 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-zinc-700 hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors"
            >
              End Interview Early
            </button>
            <button
              type="submit"
              disabled={submitting || !answerText.trim()}
              className={`px-6 py-2.5 font-semibold rounded-xl shadow flex items-center gap-2 transition-all ${
                submitting || !answerText.trim()
                  ? 'bg-indigo-300 cursor-not-allowed text-white dark:bg-zinc-700 dark:text-zinc-400'
                  : 'bg-indigo-600 hover:bg-indigo-700 text-white dark:bg-amber-400 dark:text-black dark:hover:bg-amber-300'
              }`}
            >
              {submitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Recording Answer...</span>
                </>
              ) : (
                <>
                  <span>{isLastQuestion ? 'Complete Interview' : 'Submit & Next Question'}</span>
                  <Send className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
