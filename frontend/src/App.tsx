import { useCallback, useEffect, useState } from "react";
import { Clock, Home } from "lucide-react";
import { ANIMATION_CSS } from "./utils/animation";
import { MOCK_HISTORY } from "./data/mockHistory";
import { PageKey, LogEntry } from "./types";
import { Sidebar, Topbar, BottomNav } from "./components";
import { HomePage } from "./pages/HomePage";
import { HistoryPage } from "./pages/HistoryPage";
import { DetailPage } from "./pages/DetailPage";

// Main application shell that controls page navigation and shared layout.
export default function App() {
  const [page, setPage] = useState<PageKey>("home");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);
  const [pageKey, setPageKey] = useState(0);

  const liveData = MOCK_HISTORY[0];

  useEffect(() => {
    const style = document.createElement("style");
    style.textContent = ANIMATION_CSS;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
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
              history={MOCK_HISTORY}
              onViewHistory={() => navigateTo("history")}
              onSelectLog={handleSelectLog}
            />
          )}

          {page === "history" && (
            <HistoryPage key={pageKey} history={MOCK_HISTORY} onSelect={handleSelectLog} />
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
