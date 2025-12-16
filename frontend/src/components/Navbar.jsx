import React from 'react';
import { useConnectionStatus } from '../hooks/useConnectionStatus';

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
    if (checking) return '檢查中...';
    return status.connected ? '已連接' : '未連接';
  };

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${getIndicatorClass()} shadow-glass-sm`} />
      <span className="text-sm font-medium text-glass-text-primary">
        {label}: <span className="font-normal text-glass-text-secondary">{getStatusText()}</span>
      </span>
    </div>
  );
};

const Navbar = () => {
  const { apiStatus, ankiStatus } = useConnectionStatus();

  return (
    <nav className="sticky top-0 z-50 bg-white/60 backdrop-blur-glass-xl border-b border-white/30 shadow-glass-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Title */}
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-glass-indigo-400/60 to-glass-indigo-500/60 backdrop-blur-glass-md flex items-center justify-center text-white font-bold text-lg shadow-glass-sm">
              A
            </div>
            <h1 className="text-2xl font-semibold tracking-tight text-glass-text-primary">AnkiKor</h1>
            <div className="hidden md:flex items-center gap-3">
              <div className="w-px h-6 bg-gradient-to-b from-transparent via-glass-text-muted/30 to-transparent" aria-hidden="true" />
              <span className="text-sm text-glass-text-muted font-medium">學習儀表板</span>
            </div>
          </div>

          {/* Connection Status */}
          <div className="flex items-center gap-6">
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
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
