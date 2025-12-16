import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { checkCoverage, getTargetLists } from '../utils/api';

const CoverageContext = createContext();

export const CoverageProvider = ({ children }) => {
  const [selectedTargetList, setSelectedTargetList] = useState('');
  const [targetLists, setTargetLists] = useState([]);
  const [coverageData, setCoverageData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch available target lists on mount
  useEffect(() => {
    const fetchTargetLists = async () => {
      try {
        const data = await getTargetLists();
        setTargetLists(data.files);
        setSelectedTargetList(data.default);
      } catch (err) {
        console.error('Failed to fetch target lists:', err);
        setError('無法載入目標清單');
      }
    };

    fetchTargetLists();
  }, []);

  // Fetch coverage data whenever selected list changes
  const fetchCoverage = useCallback(async (topK = 5) => {
    if (!selectedTargetList) return;

    setLoading(true);
    setError(null);

    try {
      const data = await checkCoverage(selectedTargetList, topK);
      setCoverageData(data);
    } catch (err) {
      console.error('Failed to fetch coverage:', err);
      setError(err.response?.data?.detail || err.message || '無法載入覆蓋率數據');
    } finally {
      setLoading(false);
    }
  }, [selectedTargetList]);

  // Auto-fetch coverage when selected list changes
  useEffect(() => {
    if (selectedTargetList) {
      fetchCoverage(5); // Default to 5 missing words for dashboard view
    }
  }, [selectedTargetList, fetchCoverage]);

  // Refresh function to manually trigger a reload
  const refreshCoverage = useCallback(() => {
    return fetchCoverage(5);
  }, [fetchCoverage]);

  const value = {
    selectedTargetList,
    setSelectedTargetList,
    targetLists,
    coverageData,
    loading,
    error,
    fetchCoverage,
    refreshCoverage,
  };

  return (
    <CoverageContext.Provider value={value}>
      {children}
    </CoverageContext.Provider>
  );
};

// Custom hook to use the coverage context
export const useCoverage = () => {
  const context = useContext(CoverageContext);
  if (!context) {
    throw new Error('useCoverage must be used within a CoverageProvider');
  }
  return context;
};

export default CoverageContext;
