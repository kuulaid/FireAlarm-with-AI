import React, { useState, useEffect, useRef } from 'react';

const ManualAlarmSwitch: React.FC = () => {
  const [isActive, setIsActive] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isToggling, setIsToggling] = useState<boolean>(false);
  
  // Use a ref to track if a toggle is in progress to prevent polling from overwriting the optimistic UI
  const isTogglingRef = useRef(false);

  const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
  const API_URL = `${baseUrl}/api/alarm`; 

  // Function to pull the latest state from the backend
  const fetchCurrentStatus = async () => {
    // If the user is actively clicking the override, skip this poll
    if (isTogglingRef.current) return; 

    try {
      const res = await fetch(API_URL);
      if (res.ok) {
        const data = await res.json();
        setIsActive(data.is_active);
      }
    } catch (err) {
      console.error("Failed to fetch alarm state:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // 1. Initial fetch
    fetchCurrentStatus();

    // 2. Poll the backend every 2 seconds to keep the status live
    const intervalId = setInterval(fetchCurrentStatus, 2000);

    // 3. Cleanup on unmount
    return () => clearInterval(intervalId);
  }, [API_URL]);

  const handleToggle = async () => {
    // Block multiple clicks and lock the polling
    if (isToggling) return;
    
    setIsToggling(true);
    isTogglingRef.current = true;
    
    const newState = !isActive;
    setIsActive(newState); // Optimistic UI update for instant feedback

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ is_active: newState }),
      });

      if (!response.ok) {
        setIsActive(!newState); // Revert if backend rejects
        console.error("Failed to toggle alarm on the server.");
      }
    } catch (error) {
      setIsActive(!newState);
      console.error("Network error toggling alarm:", error);
    } finally {
      setIsToggling(false);
      // Release the lock so polling can resume on the next tick
      setTimeout(() => {
        isTogglingRef.current = false;
      }, 500); 
    }
  };

  if (isLoading) return <div className="text-slate-400 text-center animate-pulse">Syncing with system...</div>;

  return (
    <div className="flex flex-col items-center p-8 bg-slate-900 rounded-xl max-w-sm mx-auto border border-slate-700 shadow-2xl">
      <h2 className="text-xl font-semibold text-slate-200 mb-2">System Override</h2>
      <p className="text-xs text-slate-400 mb-8">Live Status Sync Active</p>
      
      <div className={`w-28 h-28 rounded-full mb-8 flex items-center justify-center transition-all duration-300 ${
        isActive 
          ? 'bg-red-500 shadow-[0_0_50px_rgba(239,68,68,0.8)] scale-105' 
          : 'bg-slate-800 shadow-inner'
      }`}>
        <span className={`font-bold text-xl tracking-wider transition-colors ${isActive ? 'text-white' : 'text-slate-500'}`}>
          {isActive ? 'ACTIVE' : 'READY'}
        </span>
      </div>

      <button
        onClick={handleToggle}
        disabled={isToggling}
        className={`w-full py-4 px-6 rounded-lg font-bold text-white tracking-wide uppercase transition-all ${
          isToggling ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[1.02]'
        } ${
          isActive 
            ? 'bg-slate-700 hover:bg-slate-600' 
            : 'bg-red-600 hover:bg-red-500'
        }`}
      >
        {isActive ? 'Deactivate Override' : 'Force Alarm On'}
      </button>
    </div>
  );
};

export default ManualAlarmSwitch;