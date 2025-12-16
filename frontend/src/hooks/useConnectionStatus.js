import { useState, useEffect } from 'react';
import { checkApiStatus, checkAnkiStatus } from '../utils/api';

export const useConnectionStatus = (intervalMs = 10000) => {
  const [apiStatus, setApiStatus] = useState({ connected: false, checking: true });
  const [ankiStatus, setAnkiStatus] = useState({ connected: false, checking: true });

  const checkStatuses = async () => {
    try {
      const [apiResult, ankiResult] = await Promise.all([
        checkApiStatus(),
        checkAnkiStatus(),
      ]);

      setApiStatus({ ...apiResult, checking: false });
      setAnkiStatus({ ...ankiResult, checking: false });
    } catch (error) {
      console.error('Error checking statuses:', error);
      setApiStatus({ connected: false, checking: false, error: error.message });
      setAnkiStatus({ connected: false, checking: false, error: error.message });
    }
  };

  useEffect(() => {
    // Check immediately on mount
    checkStatuses();

    // Set up interval for periodic checks
    const interval = setInterval(checkStatuses, intervalMs);

    return () => clearInterval(interval);
  }, [intervalMs]);

  return { apiStatus, ankiStatus, refresh: checkStatuses };
};
