import React, { useState, useEffect, useMemo } from 'react';
import { getVocabWords } from '../utils/api';
import { GlassCard, GlassBadge, GlassInput } from './GlassComponents';

const VocabList = () => {
  const [words, setWords] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWords = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await getVocabWords();
        setWords(data.words);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch vocab words:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchWords();
  }, []);

  // Filter words based on search term
  const filteredWords = useMemo(() => {
    if (!searchTerm.trim()) return words;
    return words.filter((word) =>
      word.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [words, searchTerm]);

  return (
    <GlassCard className="relative animate-fade-in">
      <div className="flex items-center gap-4 mb-8">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400/40 to-amber-500/40 backdrop-blur-glass-md flex items-center justify-center text-2xl">
          📖
        </div>
        <h3 className="card-title">已學單字列表</h3>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <label htmlFor="search-vocab" className="block font-medium mb-3 text-glass-text-primary">
          搜尋單字
        </label>
        <div className="relative">
          <input
            id="search-vocab"
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="輸入韓語單字..."
            className="w-full px-4 py-3 pr-12 bg-white/60 backdrop-blur-glass-sm border border-white/40 rounded-glass-md korean-text text-glass-text-primary placeholder-glass-text-muted/60 shadow-[inset_0_2px_8px_rgba(0,0,0,0.03)] transition-all duration-300 ease focus:bg-white/75 focus:border-glass-indigo-300/40 focus:shadow-[0_0_0_3px_rgba(139,92,246,0.1)] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading}
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-glass-text-muted hover:text-glass-text-primary font-bold transition-colors duration-200"
              aria-label="清除搜尋"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      {/* Stats Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-6 border-b border-white/20">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-glass-indigo-400 shadow-glass-sm" />
          <span className="font-medium text-glass-text-secondary">
            總計: <span className="text-glass-text-primary font-semibold">{words.length}</span> 個單字
          </span>
        </div>
        {searchTerm && (
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-amber-400 shadow-glass-sm" />
            <span className="font-medium text-glass-text-secondary">
              搜尋結果: <span className="text-glass-text-primary font-semibold">{filteredWords.length}</span> 個
            </span>
          </div>
        )}
      </div>

      {/* Words List */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="flex flex-col items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-amber-400/40 to-amber-500/40 backdrop-blur-glass-md animate-glow-pulse" />
            <span className="text-lg font-medium text-glass-text-secondary">載入中...</span>
          </div>
        </div>
      ) : error ? (
        <div className="p-5 bg-gradient-to-br from-red-50/80 to-red-100/80 backdrop-blur-glass-md border border-red-300/40 rounded-glass-lg">
          <p className="font-semibold text-red-600 mb-1">錯誤</p>
          <p className="text-sm text-glass-text-secondary">{error}</p>
        </div>
      ) : filteredWords.length === 0 ? (
        <div className="text-center py-16">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-amber-400/20 to-amber-500/20 backdrop-blur-glass-md mx-auto mb-6 flex items-center justify-center text-4xl">
            🔍
          </div>
          <p className="text-glass-text-secondary font-medium">
            {searchTerm ? '找不到符合的單字' : '尚無已學單字'}
          </p>
        </div>
      ) : (
        <div className="max-h-[500px] overflow-y-auto pr-2 -mr-2">
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {filteredWords.map((word, index) => (
              <GlassBadge
                key={index}
                variant="default"
                className="korean-text text-center py-3 hover:bg-white/60 hover:shadow-glass-sm transition-all duration-300 cursor-pointer"
              >
                {word}
              </GlassBadge>
            ))}
          </div>
        </div>
      )}
    </GlassCard>
  );
};

export default VocabList;
