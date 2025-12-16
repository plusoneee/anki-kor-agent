import React from 'react';
import { Link } from 'react-router-dom';
import Dashboard from '../components/Dashboard';
import { BauhausCard } from '../components/BauhausShapes';

const DashboardPage = () => {
  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div>
        <h1 className="page-title">學習進度儀表板</h1>
        <p className="text-retro-olive text-lg">追蹤您的韓語學習覆蓋率與進度</p>
      </div>

      {/* Main Dashboard Component */}
      <Dashboard />

      {/* Quick Action Cards */}
      <div>
        <h2 className="section-title">快速操作</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/learning?focus=vocab" className="group">
            <BauhausCard
              accentColor="blue"
              className="hover:shadow-[0_12px_0_rgba(92,64,51,0.15),0_16px_32px_rgba(92,64,51,0.2)] transition-all duration-200 cursor-pointer group-hover:translate-y-[-4px]"
            >
              <div className="flex items-start gap-4">
                <div className="text-4xl">📝</div>
                <div className="flex-1">
                  <h3 className="card-title mb-2">
                    快速建立單字卡片
                  </h3>
                  <p className="text-retro-olive">
                    立即添加新的韓語單字到 Anki
                  </p>
                  <div className="mt-4 text-retro-avocado font-medium flex items-center gap-2">
                    前往建立
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                </div>
              </div>
            </BauhausCard>
          </Link>

          <Link to="/learning?focus=listening" className="group">
            <BauhausCard
              accentColor="red"
              className="hover:shadow-[0_12px_0_rgba(92,64,51,0.15),0_16px_32px_rgba(92,64,51,0.2)] transition-all duration-200 cursor-pointer group-hover:translate-y-[-4px]"
            >
              <div className="flex items-start gap-4">
                <div className="text-4xl">🎧</div>
                <div className="flex-1">
                  <h3 className="card-title mb-2">
                    快速建立聽力卡片
                  </h3>
                  <p className="text-retro-olive">
                    添加韓語句子進行聽力練習
                  </p>
                  <div className="mt-4 text-retro-rust font-medium flex items-center gap-2">
                    前往建立
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                </div>
              </div>
            </BauhausCard>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
