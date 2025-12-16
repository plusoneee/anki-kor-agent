import React, { useState, useEffect } from 'react';
import { getTargetLists, checkCoverage } from '../utils/api';
import { GlassCard, GlassBadge, GlassProgress } from './GlassComponents';

const TargetListManager = () => {
  const [targetLists, setTargetLists] = useState([]);
  const [selectedList, setSelectedList] = useState('');
  const [coverageData, setCoverageData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAllMissing, setShowAllMissing] = useState(false);

  useEffect(() => {
    const fetchLists = async () => {
      try {
        const data = await getTargetLists();
        setTargetLists(data.files);
        setSelectedList(data.default);
      } catch (err) {
        setError('無法載入目標清單');
        console.error('Failed to fetch target lists:', err);
      }
    };

    fetchLists();
  }, []);

  const handleCheckCoverage = async () => {
    if (!selectedList) return;

    setLoading(true);
    setError(null);

    try {
      const topK = showAllMissing ? 0 : 10;
      const data = await checkCoverage(selectedList, topK);
      setCoverageData(data);
    } catch (err) {
      setError(err.message);
      console.error('Failed to check coverage:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedList) {
      handleCheckCoverage();
    }
  }, [selectedList, showAllMissing]);

  return (
    <GlassCard className="relative animate-fade-in">
      <div className="relative">
        <div className="flex items-center gap-4 mb-8">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-glass-indigo-300/40 to-glass-indigo-400/40 backdrop-blur-glass-md flex items-center justify-center text-2xl">
            🎯
          </div>
          <h3 className="card-title">目標清單管理</h3>
        </div>

        {/* List Selector */}
        <div className="mb-8">
          <label htmlFor="target-list-selector" className="block font-medium mb-3 text-glass-text-primary">
            選擇目標清單
          </label>
          <select
            id="target-list-selector"
            value={selectedList}
            onChange={(e) => setSelectedList(e.target.value)}
            className="w-full px-5 py-3 bg-white/60 backdrop-blur-glass-sm border border-white/40 rounded-glass-md font-medium text-glass-text-primary focus:outline-none focus:bg-white/75 focus:border-glass-indigo-300/40 focus:shadow-[0_0_0_3px_rgba(139,92,246,0.1)] transition-all duration-300"
          >
            <option value="">-- 請選擇 --</option>
            {targetLists.map((file) => (
              <option key={file} value={file}>
                {file}
              </option>
            ))}
          </select>
        </div>

        {/* Coverage Summary */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-glass-indigo-300/40 to-glass-indigo-400/40 backdrop-blur-glass-md animate-glow-pulse" />
              <span className="text-lg font-medium text-glass-text-secondary">分析中...</span>
            </div>
          </div>
        ) : error ? (
          <div className="p-5 bg-gradient-to-br from-red-50/80 to-red-100/80 backdrop-blur-glass-md border border-red-300/40 rounded-glass-lg">
            <p className="font-semibold text-red-600 mb-1">錯誤</p>
            <p className="text-sm text-glass-text-secondary">{error}</p>
          </div>
        ) : (
          coverageData && (
            <>
              {/* Summary Stats */}
              <div className="grid grid-cols-3 gap-3 mb-8">
                <div className="p-4 bg-white/30 backdrop-blur-glass-sm rounded-glass-md border border-white/20">
                  <p className="text-xs text-glass-text-muted mb-1">目標</p>
                  <p className="text-xl font-semibold text-glass-text-primary">{coverageData.target_word_count}</p>
                </div>

                <div className="p-4 bg-gradient-to-br from-glass-indigo-400/20 to-glass-indigo-500/20 backdrop-blur-glass-sm rounded-glass-md border border-white/20">
                  <p className="text-xs text-glass-text-muted mb-1">已學習</p>
                  <p className="text-xl font-semibold text-glass-indigo-600">
                    {coverageData.existing_count}
                  </p>
                </div>

                <div className="p-4 bg-gradient-to-br from-glass-rose-400/20 to-glass-rose-500/20 backdrop-blur-glass-sm rounded-glass-md border border-white/20">
                  <p className="text-xs text-glass-text-muted mb-1">待學習</p>
                  <p className="text-xl font-semibold text-glass-rose-600">
                    {coverageData.missing_count}
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-8">
                <div className="flex items-center justify-between mb-3">
                  <span className="font-medium text-glass-text-secondary">覆蓋率</span>
                  <span className="text-2xl font-semibold bg-gradient-to-r from-glass-indigo-500 to-glass-indigo-600 bg-clip-text text-transparent">
                    {coverageData.coverage_percentage}%
                  </span>
                </div>
                <GlassProgress
                  value={coverageData.coverage_percentage}
                  max={100}
                  color="indigo"
                />
              </div>

              {/* Missing Words Section */}
              {coverageData.missing_count > 0 && (
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <h4 className="font-semibold text-lg text-glass-text-primary">待學習單字</h4>
                    <div className="flex items-center gap-2">
                      <input
                        id="show-all-missing"
                        type="checkbox"
                        checked={showAllMissing}
                        onChange={(e) => setShowAllMissing(e.target.checked)}
                        className="w-5 h-5 rounded-glass-sm cursor-pointer accent-glass-indigo-500 transition-all"
                      />
                      <label htmlFor="show-all-missing" className="font-medium text-sm text-glass-text-secondary cursor-pointer select-none">
                        顯示全部 ({coverageData.missing_count})
                      </label>
                    </div>
                  </div>

                  {coverageData.missing_words.length > 0 ? (
                    <div className="max-h-[400px] overflow-y-auto pr-2 -mr-2">
                      <div className="grid grid-cols-2 gap-3">
                        {coverageData.missing_words.map((word, index) => (
                          <GlassBadge
                            key={index}
                            variant="default"
                            className="korean-text text-center py-3 hover:bg-white/60 hover:shadow-glass-sm transition-all duration-300"
                          >
                            {word}
                          </GlassBadge>
                        ))}
                      </div>
                      {!showAllMissing && coverageData.missing_count > 10 && (
                        <p className="text-center text-sm text-glass-text-muted mt-6">
                          還有 {coverageData.missing_count - coverageData.missing_words.length} 個待學習單字
                        </p>
                      )}
                    </div>
                  ) : (
                    <p className="text-center text-glass-text-muted py-4">載入更多單字中...</p>
                  )}
                </div>
              )}

              {coverageData.missing_count === 0 && (
                <div className="text-center py-12">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-br from-green-400/30 to-green-500/30 backdrop-blur-glass-md mx-auto mb-6 flex items-center justify-center text-5xl">
                    🎉
                  </div>
                  <p className="text-xl font-semibold text-glass-text-primary mb-2">恭喜！</p>
                  <p className="text-glass-text-secondary">您已完成此清單的所有單字</p>
                </div>
              )}
            </>
          )
        )}
      </div>
    </GlassCard>
  );
};

export default TargetListManager;
