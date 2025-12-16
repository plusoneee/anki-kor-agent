import React from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import VocabQuickCreate from './components/VocabQuickCreate';
import ListeningQuickCreate from './components/ListeningQuickCreate';
import VocabList from './components/VocabList';
import TargetListManager from './components/TargetListManager';

function App() {
  return (
    <div className="min-h-screen relative">
      {/* Navbar */}
      <Navbar />

      {/* Main Content - Glassmorphism Layout */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 relative z-10">
        {/* Dashboard Section - Full Width */}
        <section className="mb-12">
          <Dashboard />
        </section>

        {/* Quick Create Section - 2-column Grid */}
        <section className="mb-12">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <VocabQuickCreate />
            <ListeningQuickCreate />
          </div>
        </section>

        {/* Lists Section - Asymmetric Layout */}
        <section className="mb-12">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Vocab List takes 2 columns */}
            <div className="lg:col-span-2">
              <VocabList />
            </div>

            {/* Target List Manager takes 1 column */}
            <div className="lg:col-span-1">
              <TargetListManager />
            </div>
          </div>
        </section>

        {/* Footer with subtle glassmorphism */}
        <footer className="mt-16 py-8">
          <div className="flex items-center justify-center gap-6 mb-4">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-glass-rose-300/30 to-glass-rose-400/30 backdrop-blur-glass-sm animate-float-slow" aria-hidden="true" />
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-glass-indigo-300/30 to-glass-indigo-400/30 backdrop-blur-glass-sm animate-float-slow" aria-hidden="true" style={{ animationDelay: '1s' }} />
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-glass-lavender/30 to-glass-periwinkle/30 backdrop-blur-glass-sm animate-float-slow" aria-hidden="true" style={{ animationDelay: '2s' }} />
          </div>
          <p className="text-center text-sm text-glass-text-muted font-medium">
            AnkiKor © 2024 - Glassmorphism Design
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;
