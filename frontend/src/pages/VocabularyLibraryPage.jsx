import React from 'react';
import VocabList from '../components/VocabList';
import TargetListManager from '../components/TargetListManager';

const VocabularyLibraryPage = () => {
  return (
    <div className="space-y-8">
      {/* Page Title */}
      <div className="animate-fade-in">
        <h1 className="page-title">單字庫</h1>
        <p className="text-glass-text-secondary text-lg">管理已學習的單字與目標清單</p>
      </div>

      {/* Two-Column Layout: VocabList (60%) + TargetListManager (40%) */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
        {/* Vocab List - Takes 3 columns (60%) */}
        <div className="lg:col-span-3">
          <VocabList />
        </div>

        {/* Target List Manager - Takes 2 columns (40%) */}
        <div className="lg:col-span-2">
          <TargetListManager />
        </div>
      </div>
    </div>
  );
};

export default VocabularyLibraryPage;
