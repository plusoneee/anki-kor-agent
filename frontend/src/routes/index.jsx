import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import LearningCenterPage from '../pages/LearningCenterPage';
import VocabularyLibraryPage from '../pages/VocabularyLibraryPage';

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Navigate to="/learning" replace />} />
        <Route path="/learning" element={<LearningCenterPage />} />
        <Route path="/vocabulary" element={<VocabularyLibraryPage />} />
        <Route path="*" element={<Navigate to="/learning" replace />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
