import { AlertTriangle, CheckCircle, Download, Search, Zap } from "lucide-react";
import { LogEntry } from "../types";
import { getLevelTheme } from "../utils/theme";

interface AlertBannerProps {
  data: LogEntry;
}

// Top dashboard alert that shows the latest summary and action buttons.
export function AlertBanner({ data }: AlertBannerProps) {
  const theme = getLevelTheme(data.danger_level);
  const AlertIcon = data.danger ? AlertTriangle : CheckCircle;
  const title = data.danger
    ? data.danger_level === "CRITICAL"
      ? "Critical Atmosphere Warning"
      : "Elevated Gas Levels Detected"
    : "No Hazardous Conditions Detected";

  return (
    <div className={`${theme.bgGradient} ${theme.bannerExtra} anim-banner rounded-2xl p-5 mb-5 relative overflow-hidden`}>
      <div className="flex items-center gap-1.5 text-[11px] font-bold tracking-widest uppercase text-white/80 mb-2">
        <AlertIcon className="w-3.5 h-3.5" />
        {data.danger ? `${data.danger_level} Alert` : "All Systems Nominal"}
      </div>
      <p className="font-extrabold text-white text-xl leading-snug mb-4">{title}</p>

      {data.danger && data.actions.length > 0 ? (
        <div className="flex flex-col gap-2">
          <button className={`btn-press flex items-center justify-center gap-2 bg-white font-bold text-sm py-2.5 px-4 rounded-xl w-full ${theme.textStrong}`}>
            <Zap className="w-4 h-4 flex-shrink-0" /> {data.actions[0]}
          </button>
          {data.actions[1] && (
            <button className="btn-press flex items-center justify-center gap-2 bg-white/10 border border-white/25 text-white font-semibold text-sm py-2.5 px-4 rounded-xl w-full">
              <Search className="w-4 h-4 flex-shrink-0" /> {data.actions[1]}
            </button>
          )}
        </div>
      ) : (
        <p className="text-white/80 text-sm">{data.summary}</p>
      )}

      <AlertIcon
        className="absolute right-5 top-1/2 -translate-y-1/2 text-white/[0.07] pointer-events-none select-none"
        style={{ width: 88, height: 88 }}
      />
    </div>
  );
}
