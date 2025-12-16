import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { checkCoverage, getTargetLists } from '../utils/api';
import { GlassCard, GlassBadge, GlassProgress } from './GlassComponents';

const GLASS_COLORS = {
  existing: '#818cf8', // Indigo
  missing: '#fb7185', // Rose
  background: '#a5b4fc', // Light Indigo
};

const Dashboard = () => {
  const [coverageData, setCoverageData] = useState(null);
  const [targetLists, setTargetLists] = useState([]);
  const [selectedList, setSelectedList] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch available target lists
  useEffect(() => {
    const fetchTargetLists = async () => {
      try {
        const data = await getTargetLists();
        setTargetLists(data.files);
        setSelectedList(data.default);
      } catch (err) {
        console.error('Failed to fetch target lists:', err);
      }
    };

    fetchTargetLists();
  }, []);

  // Fetch coverage data when selected list changes
  useEffect(() => {
    if (!selectedList) return;

    const fetchCoverage = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await checkCoverage(selectedList, 5);
        setCoverageData(data);
      } catch (err) {
        setError(err.message);
        console.error('Failed to fetch coverage:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCoverage();
  }, [selectedList]);

  // Prepare chart data
  const chartData = coverageData
    ? [
        { name: '已學習', value: coverageData.existing_count, color: GLASS_COLORS.existing },
        { name: '未學習', value: coverageData.missing_count, color: GLASS_COLORS.missing },
      ]
    : [];

  return (
    <div className="space-y-8">
      {/* Coverage Statistics */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="flex flex-col items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-glass-indigo-300/40 to-glass-indigo-400/40 backdrop-blur-glass-md animate-glow-pulse" />
            <span className="text-lg font-medium text-glass-text-secondary">載入中...</span>
          </div>
        </div>
      ) : error ? (
        <GlassCard variant="emphasis" className="animate-slide-up">
          <div className="flex items-center gap-3">
            <span className="text-glass-rose-500 font-bold text-xl">✗</span>
            <p className="text-glass-text-primary font-medium">錯誤: {error}</p>
          </div>
        </GlassCard>
      ) : (
        coverageData && (
          <GlassCard className="animate-slide-up">
            {/* Header with Target List Selector */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-glass-indigo-300/40 to-glass-indigo-400/40 backdrop-blur-glass-md flex items-center justify-center text-2xl">
                  📊
                </div>
                <h3 className="card-title">覆蓋率視覺化</h3>
              </div>
              <div className="flex items-center gap-3">
                <label htmlFor="target-list" className="text-sm font-medium text-glass-text-secondary whitespace-nowrap">
                  目標清單
                </label>
                <select
                  id="target-list"
                  value={selectedList}
                  onChange={(e) => setSelectedList(e.target.value)}
                  className="px-4 py-2 bg-white/60 backdrop-blur-glass-sm border border-white/40 rounded-glass-md text-sm font-medium text-glass-text-primary focus:outline-none focus:bg-white/75 focus:border-glass-indigo-300/40 focus:shadow-[0_0_0_3px_rgba(139,92,246,0.1)] transition-all duration-300"
                >
                  {targetLists.map((file) => (
                    <option key={file} value={file}>
                      {file}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Two Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Left Column: Chart and Progress */}
              <div className="space-y-6">
                {/* Chart */}
                <div>
                  <ResponsiveContainer width="100%" height={280}>
                    <PieChart>
                      <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={70}
                        outerRadius={100}
                        paddingAngle={2}
                        dataKey="value"
                      >
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                {/* Progress Bar */}
                <div className="p-6 bg-white/20 backdrop-blur-glass-sm rounded-glass-lg border border-white/20">
                  <div className="mb-4">
                    <p className="text-sm text-glass-text-muted mb-2 font-medium">覆蓋率</p>
                    <p className="text-5xl font-semibold bg-gradient-to-r from-glass-indigo-500 to-glass-indigo-600 bg-clip-text text-transparent">
                      {coverageData.coverage_percentage}%
                    </p>
                  </div>
                  <GlassProgress
                    value={coverageData.coverage_percentage}
                    max={100}
                    color="indigo"
                  />
                  <div className="flex items-center gap-4 text-sm mt-4">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-glass-indigo-400" />
                      <span className="text-glass-text-secondary">已學習</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-glass-rose-400" />
                      <span className="text-glass-text-secondary">未學習</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Statistics (Vertical Stack) */}
              <div className="space-y-4">
                <h4 className="font-semibold text-lg text-glass-text-primary mb-2">統計資訊</h4>

                {/* Target Count */}
                <div className="p-6 bg-white/30 backdrop-blur-glass-sm rounded-glass-lg border border-white/20 hover:bg-white/40 transition-all duration-300">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-full bg-gradient-to-br from-glass-indigo-300/50 to-glass-indigo-400/50 backdrop-blur-glass-md flex items-center justify-center text-glass-indigo-700 font-bold text-2xl flex-shrink-0">
                      📚
                    </div>
                    <div>
                      <p className="text-sm text-glass-text-muted mb-1">目標單字數</p>
                      <p className="text-4xl font-semibold text-glass-text-primary">{coverageData.target_word_count}</p>
                    </div>
                  </div>
                </div>

                {/* Existing Count */}
                <div className="p-6 bg-white/30 backdrop-blur-glass-sm rounded-glass-lg border border-white/20 hover:bg-white/40 transition-all duration-300">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-full bg-gradient-to-br from-glass-indigo-400/50 to-glass-indigo-500/50 backdrop-blur-glass-md flex items-center justify-center text-glass-indigo-800 font-bold text-2xl flex-shrink-0">
                      ✓
                    </div>
                    <div>
                      <p className="text-sm text-glass-text-muted mb-1">已學單字數</p>
                      <p className="text-4xl font-semibold bg-gradient-to-r from-glass-indigo-500 to-glass-indigo-600 bg-clip-text text-transparent">
                        {coverageData.existing_count}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Missing Count */}
                <div className="p-6 bg-white/30 backdrop-blur-glass-sm rounded-glass-lg border border-white/20 hover:bg-white/40 transition-all duration-300">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-full bg-gradient-to-br from-glass-rose-300/50 to-glass-rose-400/50 backdrop-blur-glass-md flex items-center justify-center text-glass-rose-700 font-bold text-2xl flex-shrink-0">
                      ⋯
                    </div>
                    <div>
                      <p className="text-sm text-glass-text-muted mb-1">待學單字數</p>
                      <p className="text-4xl font-semibold bg-gradient-to-r from-glass-rose-400 to-glass-rose-500 bg-clip-text text-transparent">
                        {coverageData.missing_count}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </GlassCard>
        )
      )}

      {/* Missing Words Preview */}
      {coverageData && coverageData.missing_words.length > 0 && (
        <GlassCard variant="subtle" className="animate-slide-up">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400/40 to-amber-500/40 backdrop-blur-glass-md flex items-center justify-center text-2xl">
              📝
            </div>
            <h3 className="card-title">待學單字預覽（前5個）</h3>
          </div>
          <div className="flex flex-wrap gap-3">
            {coverageData.missing_words.map((word, index) => (
              <GlassBadge
                key={index}
                variant="default"
                className="korean-text text-base px-5 py-3 hover:bg-white/60 hover:shadow-glass-sm transition-all duration-300 cursor-pointer"
              >
                {word}
              </GlassBadge>
            ))}
          </div>
        </GlassCard>
      )}
    </div>
  );
};

export default Dashboard;
