import { useState, useEffect, useCallback } from "react";
import "./styles/index.css";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import BottomNav from "./components/BottomNav";
import HomePage from "./pages/HomePage";
import HistoryPage from "./pages/HistoryPage";
import DetailPage from "./pages/DetailPage";
import { MOCK_HISTORY } from "./data/mockData";

export default function App() {
  const [page, setPage]               = useState("home");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedLog, setSelectedLog] = useState(null);
  const liveData = MOCK_HISTORY[0];

  useEffect(() => {
    document.body.style.margin = "0";
    document.body.style.padding = "0";
  }, []);

  const handleSelectLog = useCallback((log) => {
    setSelectedLog(log);
    setPage("detail");
    setSidebarOpen(false);
  }, []);

  const navTo = (p) => { 
    setPage(p); 
    setSidebarOpen(false); 
  };

  const titles = { 
    home: "Dashboard", 
    history: "Detection History", 
    detail: "Log Detail" 
  };

  return (
    <div className="shell">
      {/* Sidebar and Overlay */}
      <Sidebar 
        open={sidebarOpen} 
        page={page} 
        onNavTo={navTo} 
        onClose={() => setSidebarOpen(false)} 
      />

      {/* Main */}
      <div className="main">
        {/* Topbar */}
        <Topbar 
          page={page} 
          onBurgerClick={() => setSidebarOpen(o => !o)} 
          titles={titles}
        />

        {/* Content */}
        <div className="content">
          {page === "home" && (
            <HomePage
              liveData={liveData}
              history={MOCK_HISTORY}
              onViewHistory={() => navTo("history")}
              onSelectLog={handleSelectLog}
            />
          )}
          {page === "history" && (
            <HistoryPage history={MOCK_HISTORY} onSelect={handleSelectLog} />
          )}
          {page === "detail" && selectedLog && (
            <DetailPage log={selectedLog} onBack={() => navTo("history")} />
          )}
        </div>
      </div>

      {/* Bottom Nav — mobile only */}
      <BottomNav page={page} onNavTo={navTo} />
    </div>
  );
}
