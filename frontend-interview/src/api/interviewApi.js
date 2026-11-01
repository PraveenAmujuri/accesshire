const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Helper to extract human-readable error messages from API responses,
 * including FastAPI 422 validation detail arrays.
 */
function extractErrorMessage(data) {
  if (!data) return 'Request failed';
  if (typeof data === 'string') return data;
  if (Array.isArray(data.detail)) {
    // FastAPI validation errors: [{ loc: [...], msg: "Field required", type: "..." }]
    return data.detail
      .map((item) => (typeof item === 'object' && item.msg ? `${item.loc?.slice(1).join('.') || 'Field'}: ${item.msg}` : String(item)))
      .join(', ');
  }
  if (typeof data.detail === 'string') {
    return data.detail;
  }
  if (typeof data.message === 'string') {
    return data.message;
  }
  return JSON.stringify(data);
}

/**
 * Standard HTTP helper with JWT Bearer auth and error unwrapping
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem('accesshire_token');

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const config = {
    ...options,
    headers,
  };

  try {
    const res = await fetch(url, config);
    const contentType = res.headers.get('content-type');
    const isJson = contentType && contentType.includes('application/json');
    const data = isJson ? await res.json() : await res.text();

    if (!res.ok) {
      throw new Error(extractErrorMessage(data));
    }
    return data;
  } catch (err) {
    // If backend is offline or network error occurs
    if (err.name === 'TypeError' && err.message.includes('fetch')) {
      throw new Error('Unable to connect to the AccessHire backend service (http://localhost:8000). Please ensure the FastAPI server is running.');
    }
    throw err;
  }
}

export const interviewApi = {
  // Authentication
  register: (payload) =>
    request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  login: (payload) =>
    request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getProfile: () =>
    request('/users/me'),

  updatePreferences: (preferences) =>
    request('/users/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences),
    }),

  // Start a new interview session
  startSession: (payload) =>
    request('/interviews/start', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  // Get session status and details
  getSession: (sessionId) =>
    request(`/interviews/${sessionId}`),

  // Get current active question for the turn
  getCurrentQuestion: (sessionId) =>
    request(`/interviews/${sessionId}/current-question`),

  // Submit candidate answer for current turn
  submitAnswer: (sessionId, payload) =>
    request(`/interviews/${sessionId}/submit-answer`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  // Conclude interview session early
  endSession: (sessionId) =>
    request(`/interviews/${sessionId}/end`, {
      method: 'POST',
    }),

  // List candidate's interview sessions for dashboard
  listSessions: () =>
    request('/interviews'),

  // Get full session report and transcript
  getReport: (sessionId) =>
    request(`/reports/${sessionId}`),

  // Upload resume file (PDF or DOCX)
  uploadResume: async (file) => {
    const token = localStorage.getItem('accesshire_token');
    const formData = new FormData();
    formData.append('file', file);
    const url = `${API_BASE_URL}/resumes/upload`;
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(extractErrorMessage(data));
      }
      return data;
    } catch (err) {
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        throw new Error('Unable to connect to the AccessHire backend service.');
      }
      throw err;
    }
  },

  // Agent 1: Candidate & Job Analysis
  analyzeCandidateJob: (payload) =>
    request('/analysis/candidate-job', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
