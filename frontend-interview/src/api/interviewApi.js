const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Standard HTTP helper with error unwrapping
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const res = await fetch(url, config);
    const contentType = res.headers.get('content-type');
    const isJson = contentType && contentType.includes('application/json');
    const data = isJson ? await res.json() : await res.text();

    if (!res.ok) {
      const errorMessage = (data && data.detail) || (typeof data === 'string' ? data : 'Request failed');
      throw new Error(errorMessage);
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
};
