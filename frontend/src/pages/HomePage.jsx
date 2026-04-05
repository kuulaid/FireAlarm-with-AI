import AlertBanner from "../components/AlertBanner";
import SensorGrid from "../components/SensorGrid";
import { formatTime } from "../utils/helpers";

export default function HomePage({ liveData, history, onViewHistory, onSelectLog }) {
  return (
    <div>
      <AlertBanner data={liveData} />

      <div className="sechdr">
        <div className="sec-title">Live Sensor Readings</div>
        <div style={{ fontSize: 11, color: "var(--muted)" }}>Auto-refresh</div>
      </div>

      <SensorGrid sensors={liveData.sensors} />

      <div className="sechdr">
        <div className="sec-title">Recent Activity</div>
        <button className="sec-link" onClick={onViewHistory}>View All Logs</button>
      </div>

      <div className="actlist">
        {history.slice(0, 3).map(h => {
          const dc  = h.danger_level === "CRITICAL" ? "D" : h.danger_level === "MEDIUM" ? "W" : "S";
          const emo = h.danger_level === "CRITICAL" ? "🚨" : h.danger_level === "MEDIUM" ? "⚠️" : "✅";
          return (
            <div className="act" key={h.id} onClick={() => onSelectLog(h)}>
              <div className={`act-dot ${dc}`}>{emo}</div>
              <div className="act-body">
                <div className="act-title">{h.summary}</div>
                <div className="act-meta">{formatTime(h.timestamp)} · Sensor MQ-7</div>
              </div>
              <div className="chev">›</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
