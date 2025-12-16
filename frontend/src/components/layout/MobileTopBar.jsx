import React from 'react';
import { useLocation } from 'react-router-dom';

const getPageTitle = (pathname) => {
  switch (pathname) {
    case '/learning':
      return '學習中心';
    case '/vocabulary':
      return '單字庫';
    default:
      return 'AnkiKor';
  }
};

const MobileTopBar = ({ onMenuClick }) => {
  const location = useLocation();
  const pageTitle = getPageTitle(location.pathname);

  return (
    <div className="bg-white/70 backdrop-blur-glass-xl p-4 flex items-center gap-4 border-b border-white/30 shadow-glass-md sticky top-0 z-40">
      {/* Hamburger Menu Button */}
      <button
        onClick={onMenuClick}
        className="p-2 hover:bg-white/50 rounded-glass-md transition-all duration-300 active:scale-95 text-glass-text-primary backdrop-blur-glass-sm"
        aria-label="開啟選單"
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          strokeWidth={2.5}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      {/* Page Title */}
      <h1 className="text-xl flex-1 text-glass-text-primary font-semibold tracking-tight">{pageTitle}</h1>
    </div>
  );
};

export default MobileTopBar;
