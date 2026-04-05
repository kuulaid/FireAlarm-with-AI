import { AlertTriangle, CheckCircle, ChevronRight } from "lucide-react";
import { LogEntry } from "../types";
import { getLevelTheme } from "../utils/theme";
import { formatTime } from "../utils/format";

interface ActivityRowProps {
  entry: LogEntry;
  onClick: () => void;
  showTime?: boolean;
  showSubLabel?: boolean;
}

// A list row used for recent history items and previous scans.
export function ActivityRow({ entry, onClick, showTime = false, showSubLabel = false }: ActivityRowProps) {
  const theme = getLevelTheme(entry.danger_level);
  const RowIcon = entry.danger ? AlertTriangle : CheckCircle;
  const titleClass = entry.danger ? theme.textStrong : "text-slate-800";

  const subLabel = showSubLabel
    ? entry.suspected_gas !== "None"
      ? entry.suspected_gas
      : `CO: ${entry.sensors?.mq7 ?? "--"} ppm`
    : `${formatTime(entry.timestamp)} · Sensor MQ-7`;

  return (
    <button
      onClick={onClick}
      className="hover-lift hover-chev anim-item flex items-center gap-3 bg-white border border-slate-200 rounded-2xl p-3.5 text-left w-full transition-colors hover:border-slate-300"
    >
      <div className={`w-10 h-10 rounded-full ${theme.bgMedium} flex items-center justify-center flex-shrink-0`}>
        <RowIcon className={`w-5 h-5 ${theme.iconColor}`} />
      </div>
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-semibold truncate ${titleClass}`}>{entry.summary}</p>
        <p className="text-xs text-slate-400 mt-0.5">{subLabel}</p>
      </div>
      {showTime && (
        <span className="text-[11px] text-slate-400 whitespace-nowrap flex-shrink-0">{formatTime(entry.timestamp)}</span>
      )}
      <ChevronRight className="chev-icon w-4 h-4 text-slate-300 flex-shrink-0" />
    </button>
  );
}
