import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import VocabQuickCreate from '../components/VocabQuickCreate';
import ListeningQuickCreate from '../components/ListeningQuickCreate';
import { GlassCard } from '../components/GlassComponents';

const LearningCenterPage = () => {
  const [searchParams] = useSearchParams();
  const [focusSection, setFocusSection] = useState(null);
  const [tipsExpanded, setTipsExpanded] = useState(() => {
    // Load expanded state from localStorage, default to true for first-time users
    const saved = localStorage.getItem('learningTipsExpanded');
    return saved === null ? true : saved === 'true';
  });

  useEffect(() => {
    const focus = searchParams.get('focus');
    if (focus) {
      setFocusSection(focus);
      // Scroll to the focused section after a short delay
      setTimeout(() => {
        const element = document.getElementById(`${focus}-section`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    }
  }, [searchParams]);

  const toggleTips = () => {
    const newState = !tipsExpanded;
    setTipsExpanded(newState);
    localStorage.setItem('learningTipsExpanded', newState.toString());
  };

  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div className="animate-fade-in">
        <h1 className="page-title">學習中心</h1>
        <p className="text-glass-text-secondary text-lg">快速建立新的單字卡片和聽力練習</p>
      </div>

      {/* Collapsible Tips Section - At Top */}
      <GlassCard variant="subtle" className="animate-slide-up">
        <button
          onClick={toggleTips}
          className="w-full flex items-center justify-between gap-4 group cursor-pointer"
          aria-expanded={tipsExpanded}
          aria-controls="tips-content"
        >
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-amber-400/40 to-amber-500/40 backdrop-blur-glass-md flex items-center justify-center text-2xl transition-transform duration-300 group-hover:scale-110">
              💡
            </div>
            <h3 className="card-title text-left">使用提示</h3>
          </div>
          <div className={`text-glass-text-secondary transition-all duration-300 ${tipsExpanded ? 'rotate-180' : 'rotate-0'}`}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>

        <div
          id="tips-content"
          className={`overflow-hidden transition-all duration-500 ease-in-out ${
            tipsExpanded ? 'max-h-96 opacity-100 mt-6' : 'max-h-0 opacity-0 mt-0'
          }`}
        >
          <ul className="space-y-3 text-glass-text-primary">
            <li className="flex items-start gap-3">
              <span className="text-glass-indigo-500 font-bold text-xl flex-shrink-0">•</span>
              <span><strong className="text-glass-text-primary">單字卡片</strong>：輸入韓語單字，系統會自動生成意思、詞性和例句</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-glass-rose-500 font-bold text-xl flex-shrink-0">•</span>
              <span><strong className="text-glass-text-primary">聽力卡片</strong>：輸入韓語句子，可選擇性提供中文翻譯，或讓 AI 自動翻譯</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="text-amber-500 font-bold text-xl flex-shrink-0">•</span>
              <span><strong className="text-glass-text-primary">強制更新</strong>：勾選後可更新已存在的卡片</span>
            </li>
          </ul>
        </div>
      </GlassCard>

      {/* Quick Create Forms Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Vocabulary Quick Create */}
        <div id="vocab-section" className={focusSection === 'vocab' ? 'ring-4 ring-glass-indigo-300/40 rounded-glass-lg' : ''}>
          <VocabQuickCreate />
        </div>

        {/* Listening Quick Create */}
        <div id="listening-section" className={focusSection === 'listening' ? 'ring-4 ring-glass-rose-300/40 rounded-glass-lg' : ''}>
          <ListeningQuickCreate />
        </div>
      </div>
    </div>
  );
};

export default LearningCenterPage;
