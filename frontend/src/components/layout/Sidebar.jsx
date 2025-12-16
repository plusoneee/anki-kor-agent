import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useConnectionStatus } from '../../hooks/useConnectionStatus';

const navigationItems = [
  {
    path: '/learning',
    label: '學習中心',
    icon: '✏️',
  },
  {
    path: '/vocabulary',
    label: '單字庫',
    icon: '📚',
  },
];

const StatusIndicator = ({ label, status, checking }) => {
  const getIndicatorClass = () => {
    if (checking) {
      return 'bg-gradient-to-br from-amber-400/60 to-amber-500/60 animate-glow-pulse';
    }
    return status.connected
      ? 'bg-gradient-to-br from-green-400/60 to-green-500/60'
      : 'bg-gradient-to-br from-glass-rose-400/60 to-glass-rose-500/60';
  };

  const getStatusText = () => {
    if (checking) return '檢查中';
    return status.connected ? '已連接' : '未連接';
  };

  return (
    <div className="flex items-center gap-2 text-sm">
      <div className={`w-2 h-2 rounded-full ${getIndicatorClass()} shadow-glass-sm`} />
      <span className="font-medium text-glass-text-primary">
        {label}: <span className="font-normal text-glass-text-secondary">{getStatusText()}</span>
      </span>
    </div>
  );
};

const Sidebar = ({ isOpen, onClose, isMobile }) => {
  const location = useLocation();
  const { apiStatus, ankiStatus } = useConnectionStatus();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <>
      {/* Sidebar */}
      <aside
        className={`
          ${isMobile ? 'fixed' : 'relative'}
          ${isMobile && !isOpen ? '-translate-x-full' : 'translate-x-0'}
          h-full w-[280px]
          bg-white/70 backdrop-blur-glass-xl
          border-r border-white/30
          transition-all duration-300 ease-in-out
          ${isMobile ? 'z-50' : 'z-10'}
          flex flex-col
          shadow-glass-lg
        `}
      >
        {/* Logo and Title */}
        <div className="p-6 border-b border-white/20">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-glass-indigo-400/60 to-glass-indigo-500/60 backdrop-blur-glass-md flex-shrink-0 flex items-center justify-center text-white text-xl font-bold shadow-glass-md">
              A
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-glass-text-primary tracking-tight">AnkiKor</h1>
              <p className="text-sm text-glass-text-muted font-medium">韓語學習助手</p>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 py-6 px-4 overflow-y-auto">
          {navigationItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={({ isActive: isActivePath }) => `
                flex items-center gap-3 px-4 py-4 mb-2
                rounded-glass-lg transition-all duration-300
                font-medium
                ${isActivePath || isActive(item.path)
                  ? 'bg-gradient-to-br from-glass-indigo-400/60 to-glass-indigo-500/60 text-white shadow-glass-glow backdrop-blur-glass-md'
                  : 'bg-white/30 text-glass-text-primary hover:bg-white/50 hover:shadow-glass-sm backdrop-blur-glass-sm'
                }
              `}
            >
              <span className="text-2xl flex-shrink-0">{item.icon}</span>
              <span className="text-base">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Connection Status */}
        <div className="mt-auto border-t border-white/20 p-5 space-y-3 bg-white/20 backdrop-blur-glass-sm">
          <StatusIndicator
            label="API"
            status={apiStatus}
            checking={apiStatus.checking}
          />
          <StatusIndicator
            label="Anki"
            status={ankiStatus}
            checking={ankiStatus.checking}
          />
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
