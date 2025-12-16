import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Status checks
export const checkApiStatus = async () => {
  try {
    const response = await api.get('/');
    return { connected: true, data: response.data };
  } catch (error) {
    return { connected: false, error: error.message };
  }
};

export const checkAnkiStatus = async () => {
  try {
    const response = await axios.post(ANKI_CONNECT_URL, {
      action: 'version',
      version: 6,
    });
    return { connected: true, version: response.data.result };
  } catch (error) {
    return { connected: false, error: error.message };
  }
};

// Vocabulary APIs
export const getVocabWords = async () => {
  const response = await api.get('/vocab/words');
  return response.data;
};

export const createVocabCard = async (word, forceUpdate = false) => {
  const response = await api.post('/vocab', { word, force_update: forceUpdate });
  return response.data;
};

export const createVocabCardsBatch = async (words, forceUpdate = false) => {
  const response = await api.post('/vocab/batch', { words, force_update: forceUpdate });
  return response.data;
};

export const getTargetLists = async () => {
  const response = await api.get('/vocab/targets');
  return response.data;
};

export const checkCoverage = async (file = null, topK = 10) => {
  const params = {};
  if (file) params.file = file;
  if (topK) params.top_k = topK;

  const response = await api.get('/vocab/coverage', { params });
  return response.data;
};

// Listening APIs
export const createListeningCard = async (koreanSentence, chineseTranslation = null, forceUpdate = false) => {
  const response = await api.post('/listening', {
    korean_sentence: koreanSentence,
    chinese_translation: chineseTranslation,
    force_update: forceUpdate,
  });
  return response.data;
};

export const createListeningCardsBatch = async (sentences, forceUpdate = false) => {
  const response = await api.post('/listening/batch', {
    sentences,
    force_update: forceUpdate,
  });
  return response.data;
};

export default api;
