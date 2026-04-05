import { AlertTriangle, CheckCircle, Clock, Download, Info, Shield } from "lucide-react";
import { LogEntry } from "../types";
import { ActivityRow, InfoBlock } from "../components";
import { getLevelTheme } from "../utils/theme";

interface HistoryPageProps {
  history: LogEntry[];
  loading: boolean;
  onSelect: (log: LogEntry) => void;
}

// History page showing all saved detection events and summary details for the latest event.
export function HistoryPage({ history, loading, onSelect }: HistoryPageProps) {
  if (loading) {
    return (
      <div className="anim-page rounded-2xl bg-white p-6 text-center text-slate-500 shadow-sm">
        Loading history from the backend...
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="anim-page rounded-2xl bg-white p-6 text-center text-slate-500 shadow-sm">
        No history is available yet. Check back after the system records more readings.
      </div>
    );
  }

  const latest = history[0];
  const theme = getLevelTheme(latest.danger_level);
  const StatusIcon = latest.danger ? AlertTriangle : CheckCircle;

  return (
    <div className="anim-page">
      <div className="bg-white border border-slate-200 rounded-2xl p-5 mb-5 anim-item">
        <span className={`inline-flex items-center gap-1.5 text-[10px] font-bold tracking-wider uppercase px-3 py-1 rounded-full mb-4 ${theme.pillClass}`}>
          <StatusIcon className="w-3 h-3" />
          {latest.danger ? "Critical Alert" : "All Clear"}
        </span>

        <p className="text-[11px] font-semibold tracking-wider uppercase text-slate-400 mb-1 flex items-center gap-1.5">
          <AlertTriangle className="w-3.5 h-3.5" /> Carbon Monoxide (CO)
        </p>
        <div className="flex items-baseline gap-1.5 mb-2">
          <span className={`font-extrabold text-5xl leading-none tracking-tight ${theme.textStrong}`}>
            {latest.sensors?.mq7 ?? "--"}
          </span>
          <span className="text-lg text-slate-400">ppm</span>
        </div>
        <p className="text-sm font-semibold text-slate-800 mb-1">{latest.summary}</p>
        <p className="text-xs text-slate-400 flex items-center gap-1">
          <Clock className="w-3 h-3" />
          Recorded: {new Date(latest.timestamp).toLocaleString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}
        </p>

        <div className="mt-5 bg-slate-50 border border-slate-200 rounded-xl p-4">
          <p className="font-bold text-slate-800 text-sm mb-2">Complete Info</p>

          <InfoBlock icon={<Info className="w-4 h-4 text-blue-500" />} iconBg="bg-blue-50" label="Summary &amp; Risks">
            <p className="text-xs text-slate-600 leading-relaxed">
              Danger: <span className={`font-bold ${theme.textStrong}`}>{latest.danger_level}</span>. {latest.summary}
            </p>
          </InfoBlock>

          {latest.actions.length > 0 && (
            <InfoBlock icon={<Shield className="w-4 h-4 text-teal-500" />} iconBg="bg-teal-50" label="Recommended Action" noBorder>
              <p className="text-xs text-slate-600 leading-relaxed">
                Immediate action: <span className="text-teal-600 font-semibold">{latest.actions[0]}</span>. {latest.actions.slice(1).join(". ")}
              </p>
            </InfoBlock>
          )}

          <div className="flex justify-end pt-4 mt-2 border-t border-slate-200">
            <button className="btn-press flex items-center gap-1.5 text-xs font-semibold tracking-wider uppercase text-slate-600 border border-slate-200 rounded-lg px-3 py-2 hover:bg-slate-100 transition-colors">
              <Download className="w-3.5 h-3.5" /> Export Log
            </button>
          </div>
        </div>
      </div>

      <p className="text-[11px] font-bold tracking-widest uppercase text-slate-400 mb-3 anim-item">Previous Scans</p>

      <div className="flex flex-col gap-2">
        {history.slice(1).map((entry) => (
          <ActivityRow key={entry.id} entry={entry} onClick={() => onSelect(entry)} showTime showSubLabel />
        ))}
      </div>

      <p className="text-center text-[11px] font-semibold tracking-widest uppercase text-slate-400 mt-5 py-3 cursor-pointer hover:text-slate-600 transition-colors anim-item">
        View Archives (2024-Q3)
      </p>
    </div>
  );
}
