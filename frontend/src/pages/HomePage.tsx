import { Radio } from "lucide-react";
import { LogEntry } from "../types";
import { AlertBanner, ActivityRow, SensorGrid } from "../components";

interface HomePageProps {
  liveData: LogEntry;
  history: LogEntry[];
  loading: boolean;
  error: string | null;
  onViewHistory: () => void;
  onSelectLog: (log: LogEntry) => void;
}

// Dashboard home page, showing the current alert and the latest sensor readings.
export function HomePage({ liveData, history, loading, error, onViewHistory, onSelectLog }: HomePageProps) {
  if (loading) {
    return (
      <div className="anim-page rounded-2xl bg-white p-6 text-center text-slate-500 shadow-sm">
        Loading dashboard data from the backend...
      </div>
    );
  }

  return (
    <div className="anim-page">
      {error && (
        <div className="rounded-2xl bg-orange-50 border border-orange-200 p-4 mb-5 text-sm text-orange-700">
          {error}
        </div>
      )}
      <AlertBanner data={liveData} />

      <div className="flex items-center justify-between mb-3 anim-item">
        <p className="text-[11px] font-bold tracking-widest uppercase text-slate-400">Live Sensor Readings</p>
        <div className="flex items-center gap-1 text-[11px] text-slate-400">
          <Radio className="w-3 h-3" /> Auto-refresh
        </div>
      </div>

      <SensorGrid sensors={liveData.sensors} />

      <div className="flex items-center justify-between mb-3 anim-item">
        <p className="text-[11px] font-bold tracking-widest uppercase text-slate-400">Recent Activity</p>
        <button
          className="btn-press text-[11px] font-bold tracking-wider uppercase text-blue-500 hover:text-blue-600 transition-colors"
          onClick={onViewHistory}
        >
          View All Logs
        </button>
      </div>

      {history.length === 0 ? (
        <div className="rounded-2xl bg-slate-50 border border-slate-200 p-5 text-sm text-slate-500">
          No recent activity has been recorded yet.
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          {history.slice(0, 3).map((entry) => (
            <ActivityRow key={entry.id} entry={entry} onClick={() => onSelectLog(entry)} />
          ))}
        </div>
      )}
    </div>
  );
}
