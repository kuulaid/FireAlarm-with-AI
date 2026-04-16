import { useCallback, useEffect, useState } from "react";
import { Clock, Home } from "lucide-react";
import { ANIMATION_CSS } from "./utils/animation";
import { MOCK_HISTORY } from "./data/mockHistory";
import { fetchHistory, fetchLatestAnalysis } from "./services/api";
import { PageKey, LogEntry } from "./types";
import { Sidebar, Topbar, BottomNav } from "./components";
import { HomePage } from "./pages/HomePage";
import { HistoryPage } from "./pages/HistoryPage";
import { DetailPage } from "./pages/DetailPage";

// Import your manual alarm component
import ManualAlarmSwitch from "./components/ManualAlarmSwitch"; 

export default function App() {
  // --- HIDDEN ROUTE INTERCEPTOR ---
  // If you manually type /api/alarm into the browser URL, it renders ONLY this screen.
  if (window.location.pathname === "/api/alarm") {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
        <ManualAlarmSwitch />
      </div>
    );
  }

  // --- STANDARD APP STATE ---
  const [page, setPage] = useState<PageKey>("home");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);
  const [pageKey, setPageKey] = useState(0);
  const [liveData, setLiveData] = useState<LogEntry>(MOCK_HISTORY[0]);
  const [history, setHistory] = useState<LogEntry[]>(MOCK_HISTORY);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const style = document.createElement("style");
    style.textContent = ANIMATION_CSS;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  useEffect(() => {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }

    let isInitialLoad = true;
    let previousDangerLevel: string | null = null;

    const loadData = async () => {
      if (isInitialLoad) setLoading(true);
      
      try {
        const [latest, savedHistory] = await Promise.all([fetchLatestAnalysis(), fetchHistory(50)]);
        
        if (!isInitialLoad && previousDangerLevel && previousDangerLevel !== latest.danger_level) {
          if (Notification.permission === "granted") {
            new Notification("⚠️ Fire Alarm Status Changed", {
              body: `State changed from ${previousDangerLevel} to ${latest.danger_level}. \n${latest.summary}`,
              icon: "/favicon.ico" 
            });
          }
        }
        
        previousDangerLevel = latest.danger_level;

        setLiveData(latest);
        setHistory(savedHistory.length ? savedHistory : MOCK_HISTORY);
        setError(null);
      } catch (err) {
        console.error(err);
        setError("Unable to reach backend API. Showing mock data.");
        setLiveData(MOCK_HISTORY[0]);
        setHistory(MOCK_HISTORY);
      } finally {
        if (isInitialLoad) {
          setLoading(false);
          isInitialLoad = false;
        }
      }
    };

    loadData();
    const intervalId = setInterval(loadData, 5000);
    return () => clearInterval(intervalId);
  }, []);

  const handleSelectLog = useCallback((log: LogEntry) => {
    setSelectedLog(log);
    setPage("detail");
    setPageKey((current) => current + 1);
    setSidebarOpen(false);
  }, []);

  const navigateTo = (target: PageKey) => {
    setPage(target);
    setPageKey((current) => current + 1);
    setSidebarOpen(false);
  };

  // The Override option is completely removed from the menus here
  const navItems = [
    { key: "home", pages: ["home"] as PageKey[], label: "Home", icon: <Home className="w-4 h-4" /> },
    { key: "history-detail", pages: ["history", "detail"] as PageKey[], label: "History", icon: <Clock className="w-4 h-4" /> },
  ];

  return (
    <div className="flex min-h-screen bg-slate-100 overflow-x-hidden">
      {sidebarOpen && (
        <div className="anim-overlay fixed inset-0 bg-black/50 z-[199] backdrop-blur-sm md:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      <Sidebar page={page} navItems={navItems} onNavigate={navigateTo} open={sidebarOpen} />

      <div className="flex-1 flex flex-col min-h-screen md:ml-60 w-0 min-w-0">
        <Topbar page={page} onToggleSidebar={() => setSidebarOpen((current) => !current)} />

        <main className="flex-1 p-4 md:p-7 pb-24 md:pb-8 overflow-x-hidden">
          {page === "home" && (
            <HomePage
              key={pageKey}
              liveData={liveData}
              history={history}
              loading={loading}
              error={error}
              onViewHistory={() => navigateTo("history")}
              onSelectLog={handleSelectLog}
            />
          )}

          {page === "history" && (
            <HistoryPage key={pageKey} history={history} loading={loading} onSelect={handleSelectLog} />
          )}

          {page === "detail" && selectedLog && (
            <DetailPage key={pageKey} log={selectedLog} onBack={() => navigateTo("history")} />
          )}
        </main>
      </div>

      <BottomNav page={page} navItems={navItems} onNavigate={navigateTo} />
    </div>
  );
}