import { ArrowLeft, AlertTriangle, CheckCircle, Clock, ClipboardList, Download, Info, Shield } from "lucide-react";
import { LogEntry } from "../types";
import { InfoBlock } from "../components";
import { getLevelTheme } from "../utils/theme";

interface DetailPageProps {
  log: LogEntry;
  onBack: () => void;
}

// Detail page for a selected history log entry.
export function DetailPage({ log, onBack }: DetailPageProps) {
  const theme = getLevelTheme(log.danger_level);
  const StatusIcon = log.danger ? AlertTriangle : CheckCircle;

  const snapshots = [
    { label: "MQ-7 CO", value: log.sensors.mq7, unit: "ppm", isFlame: false },
    { label: "MQ-135 AQ", value: log.sensors.mq135, unit: "ppm", isFlame: false },
    { label: "MQ-2 Comb.", value: log.sensors.mq2, unit: "ppm", isFlame: false },
    { label: "Temperature", value: log.sensors.temp, unit: "°C", isFlame: false },
    { label: "Humidity", value: log.sensors.humidity, unit: "%", isFlame: false },
    { label: "Flame", value: log.sensors.flame ? "YES" : "NO", unit: "", isFlame: true },
  ] as const;

  return (
    <div className="anim-page">
      <button
        onClick={onBack}
        className="btn-press flex items-center gap-1.5 text-blue-500 text-sm font-semibold pb-4 hover:text-blue-600 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to History
      </button>

      <div className={`border rounded-2xl p-5 mb-4 anim-item ${log.danger ? `${theme.bgSoft} ${theme.border}` : "bg-white border-slate-200"}`}>
        <span className={`inline-flex items-center gap-1.5 text-[10px] font-bold tracking-wider uppercase px-3 py-1 rounded-full mb-4 ${theme.pillClass}`}>
          <StatusIcon className="w-3 h-3" /> {log.danger_level}
        </span>

        <p className="text-[11px] font-semibold tracking-wider uppercase text-slate-400 mb-1 flex items-center gap-1.5">
          <Clock className="w-3.5 h-3.5" /> {new Date(log.timestamp).toLocaleString()}
        </p>
        <div className="flex items-baseline gap-1.5 mb-2">
          <span className={`font-extrabold text-4xl leading-none tracking-tight ${theme.textStrong}`}>{log.sensors.mq7 ?? "--"}</span>
          <span className="text-base text-slate-400">ppm CO</span>
        </div>
        <p className="text-sm font-semibold text-slate-800">{log.summary}</p>
        {log.suspected_gas !== "None" && (
          <p className="text-xs text-slate-400 mt-1">
            Suspected: <span className={`font-semibold ${theme.textStrong}`}>{log.suspected_gas}</span> · Confidence: {log.confidence}%
          </p>
        )}
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 mb-4 anim-item">
        <p className="font-bold text-slate-800 text-sm mb-4">Sensor Snapshot</p>
        <div className="grid grid-cols-2 gap-2.5">
          {snapshots.map(({ label, value, unit, isFlame }) => (
            <div key={label} className="bg-slate-50 border border-slate-200 rounded-xl p-3 hover-lift">
              <p className="text-[10px] text-slate-400 uppercase tracking-wider mb-1.5">{label}</p>
              <div className="flex items-baseline gap-1">
                <span className={`font-extrabold text-xl leading-none ${isFlame ? (value === "YES" ? "text-red-500" : "text-teal-600") : "text-slate-800"}`}>
                  {value}
                </span>
                {unit && <span className="text-xs text-slate-400">{unit}</span>}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-5 mb-4 anim-item">
        <p className="font-bold text-slate-800 text-sm mb-2">Complete Analysis</p>

        <InfoBlock icon={<Info className="w-4 h-4 text-blue-500" />} iconBg="bg-blue-50" label="Summary &amp; Risks">
          <p className="text-xs text-slate-600 leading-relaxed">
            Danger level: <span className={`font-bold ${theme.textStrong}`}>{log.danger_level}</span>. {log.summary}
          </p>
        </InfoBlock>

        {log.actions.length > 0 && (
          <InfoBlock icon={<Shield className="w-4 h-4 text-teal-500" />} iconBg="bg-teal-50" label="Recommended Actions">
            <ul className="flex flex-col gap-1.5">
              {log.actions.map((action, index) => (
                <li key={index} className="text-xs text-slate-500 leading-relaxed pl-3 relative before:content-['·'] before:absolute before:left-0.5 before:text-blue-400 before:font-bold">
                  {action}
                </li>
              ))}
            </ul>
          </InfoBlock>
        )}

        <InfoBlock icon={<ClipboardList className="w-4 h-4 text-blue-500" />} iconBg="bg-blue-50" label="Analysis Reasons" noBorder>
          <ul className="flex flex-col gap-1.5">
            {log.reasons.map((reason, index) => (
              <li key={index} className="text-xs text-slate-500 leading-relaxed pl-3 relative before:content-['·'] before:absolute before:left-0.5 before:text-blue-400 before:font-bold">
                {reason}
              </li>
            ))}
          </ul>
        </InfoBlock>

        <div className="flex justify-end pt-4 mt-3 border-t border-slate-200">
          <button className="btn-press flex items-center gap-1.5 text-xs font-semibold tracking-wider uppercase text-slate-600 border border-slate-200 rounded-lg px-3 py-2 hover:bg-slate-100 transition-colors">
            <Download className="w-3.5 h-3.5" /> Export Log
          </button>
        </div>
      </div>
    </div>
  );
}
