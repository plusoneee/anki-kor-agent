import React, { useState, useRef, useEffect } from 'react';
import { createVocabCard } from '../utils/api';
import { GlassCard, GlassButton, GlassInput, GlassNotification } from './GlassComponents';

const VocabQuickCreate = () => {
  const [word, setWord] = useState('');
  const [forceUpdate, setForceUpdate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  // Auto-focus on desktop only
  useEffect(() => {
    if (window.innerWidth >= 768 && inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!word.trim()) {
      setError('請輸入單字');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await createVocabCard(word.trim(), forceUpdate);
      setResult(data);
      setWord(''); // Clear input on success
    } catch (err) {
      setError(err.response?.data?.detail || err.message || '建立失敗');
    } finally {
      setLoading(false);
    }
  };

  return (
    <GlassCard className="relative animate-fade-in" hover={false}>
      <div className="relative">
        <div className="flex items-center gap-4 mb-8">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-glass-indigo-300/40 to-glass-indigo-400/40 backdrop-blur-glass-md flex items-center justify-center text-2xl">
            ✏️
          </div>
          <h3 className="card-title">快速建立單字卡片</h3>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 pb-20 md:pb-0">
          <div>
            <label htmlFor="vocab-word" className="block font-medium mb-3 text-glass-text-primary">
              韓語單字
            </label>
            <GlassInput
              ref={inputRef}
              id="vocab-word"
              value={word}
              onChange={(e) => setWord(e.target.value)}
              placeholder="例如：학생"
              disabled={loading}
              className="korean-text"
            />
          </div>

          <div className="flex items-center gap-3">
            <input
              id="force-update"
              type="checkbox"
              checked={forceUpdate}
              onChange={(e) => setForceUpdate(e.target.checked)}
              className="w-5 h-5 rounded-glass-sm cursor-pointer accent-glass-indigo-500 transition-all"
              disabled={loading}
            />
            <label htmlFor="force-update" className="font-medium text-sm cursor-pointer text-glass-text-secondary select-none">
              強制更新（如果已存在）
            </label>
          </div>

          {/* Desktop: Regular button */}
          <div className="md:relative md:mt-4 fixed bottom-0 left-0 right-0 z-10 md:z-auto px-4 md:px-0 pb-4 md:pb-0 bg-gradient-to-t from-white/90 to-transparent md:bg-none backdrop-blur-glass-md md:backdrop-blur-0">
            <GlassButton
              type="submit"
              disabled={loading || !word.trim()}
              variant="primary"
              fullWidth
              className="py-4 text-base shadow-glass-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 rounded-full bg-white/60 backdrop-blur-glass-sm animate-glow-pulse" />
                  建立中...
                </span>
              ) : (
                '建立卡片'
              )}
            </GlassButton>
          </div>
        </form>

        {/* Result Messages - Mobile: Fixed toast, Desktop: Relative */}
        {result && (
          <div className="fixed top-4 left-4 right-4 md:relative md:top-0 md:left-0 md:right-0 md:mt-6 z-50 md:z-auto">
            <GlassNotification
              type={result.status === 'success' ? 'success' : 'warning'}
              onClose={() => setResult(null)}
            >
              <p className="font-semibold mb-2 text-glass-text-primary">
                {result.status === 'success' ? '建立成功' : '卡片已存在'}
              </p>
              <div className="text-sm space-y-1 text-glass-text-secondary">
                <p className="korean-text">單字: {word || result.word}</p>
                {result.meaning && <p>意思: {result.meaning}</p>}
                {result.anki_note_id && <p className="text-glass-text-muted">Note ID: {result.anki_note_id}</p>}
              </div>
            </GlassNotification>
          </div>
        )}

        {error && (
          <div className="mt-6">
            <GlassNotification
              type="error"
              onClose={() => setError(null)}
            >
              <p className="font-semibold text-glass-text-primary">錯誤</p>
              <p className="text-sm text-glass-text-secondary mt-1">{error}</p>
            </GlassNotification>
          </div>
        )}
      </div>
    </GlassCard>
  );
};

export default VocabQuickCreate;
