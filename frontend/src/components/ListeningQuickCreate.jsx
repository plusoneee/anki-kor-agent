import React, { useState, useRef } from 'react';
import { createListeningCard } from '../utils/api';
import { GlassCard, GlassButton, GlassNotification } from './GlassComponents';

const ListeningQuickCreate = () => {
  const [koreanSentence, setKoreanSentence] = useState('');
  const [chineseTranslation, setChineseTranslation] = useState('');
  const [showTranslation, setShowTranslation] = useState(false);
  const [forceUpdate, setForceUpdate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const koreanRef = useRef(null);
  const chineseRef = useRef(null);

  const handleKoreanInput = (e) => {
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
    setKoreanSentence(e.target.value);
  };

  const handleChineseInput = (e) => {
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
    setChineseTranslation(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!koreanSentence.trim()) {
      setError('請輸入韓語句子');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await createListeningCard(
        koreanSentence.trim(),
        chineseTranslation.trim() || null,
        forceUpdate
      );
      setResult(data);
      setKoreanSentence('');
      setChineseTranslation('');
      // Reset textarea heights
      if (koreanRef.current) koreanRef.current.style.height = 'auto';
      if (chineseRef.current) chineseRef.current.style.height = 'auto';
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
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-glass-rose-300/40 to-glass-rose-400/40 backdrop-blur-glass-md flex items-center justify-center text-2xl">
            🎧
          </div>
          <h3 className="card-title">快速建立聽力卡片</h3>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 pb-20 md:pb-0">
          <div>
            <label htmlFor="korean-sentence" className="block font-medium mb-3 text-glass-text-primary">
              韓語句子
            </label>
            <textarea
              ref={koreanRef}
              id="korean-sentence"
              value={koreanSentence}
              onChange={handleKoreanInput}
              placeholder="例如：오늘 날씨가 좋아요"
              rows={3}
              style={{ fontSize: '16px' }}
              className="w-full px-4 py-3 bg-white/60 backdrop-blur-glass-sm border border-white/40 rounded-glass-md korean-text text-glass-text-primary placeholder-glass-text-muted/60 shadow-[inset_0_2px_8px_rgba(0,0,0,0.03)] transition-all duration-300 ease resize-none overflow-hidden focus:bg-white/75 focus:border-glass-indigo-300/40 focus:shadow-[0_0_0_3px_rgba(139,92,246,0.1)] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            />
          </div>

          {/* Collapsible Translation Field */}
          <div>
            <button
              type="button"
              onClick={() => setShowTranslation(!showTranslation)}
              className="text-sm text-glass-text-secondary font-medium flex items-center gap-2 hover:text-glass-text-primary transition-colors duration-200 mb-3"
            >
              <span className="text-glass-rose-400">{showTranslation ? '▼' : '▶'}</span>
              手動輸入中文翻譯（選填，留空則會使用 AI 翻譯）
            </button>

            {showTranslation && (
              <textarea
                ref={chineseRef}
                id="chinese-translation"
                value={chineseTranslation}
                onChange={handleChineseInput}
                placeholder="例如：今天天氣很好"
                rows={3}
                style={{ fontSize: '16px' }}
                className="w-full px-4 py-3 bg-white/60 backdrop-blur-glass-sm border border-white/40 rounded-glass-md text-glass-text-primary placeholder-glass-text-muted/60 shadow-[inset_0_2px_8px_rgba(0,0,0,0.03)] transition-all duration-300 ease resize-none overflow-hidden focus:bg-white/75 focus:border-glass-indigo-300/40 focus:shadow-[0_0_0_3px_rgba(139,92,246,0.1)] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed animate-slide-up"
                disabled={loading}
              />
            )}
          </div>

          <div className="flex items-center gap-3">
            <input
              id="listening-force-update"
              type="checkbox"
              checked={forceUpdate}
              onChange={(e) => setForceUpdate(e.target.checked)}
              className="w-5 h-5 rounded-glass-sm cursor-pointer accent-glass-rose-500 transition-all"
              disabled={loading}
            />
            <label htmlFor="listening-force-update" className="font-medium text-sm cursor-pointer text-glass-text-secondary select-none">
              強制更新（如果已存在）
            </label>
          </div>

          <div className="md:relative md:mt-4 fixed bottom-0 left-0 right-0 z-10 md:z-auto px-4 md:px-0 pb-4 md:pb-0 bg-gradient-to-t from-white/90 to-transparent md:bg-none backdrop-blur-glass-md md:backdrop-blur-0">
            <GlassButton
              type="submit"
              disabled={loading || !koreanSentence.trim()}
              variant="accent"
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
                <p className="korean-text">句子: {result.korean_sentence}</p>
                {result.chinese_translation && result.chinese_translation !== '(已存在)' && (
                  <p>翻譯: {result.chinese_translation}</p>
                )}
                {result.translation_source && (
                  <p className="text-glass-text-muted">翻譯來源: {result.translation_source === 'user' ? '使用者提供' : 'AI 翻譯'}</p>
                )}
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

export default ListeningQuickCreate;
