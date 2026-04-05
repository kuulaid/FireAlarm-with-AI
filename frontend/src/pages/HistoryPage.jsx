import { levelColor, formatTime } from "../utils/helpers";

export default function HistoryPage({ history, onSelect }) {
  const latest = history[0];
  const lc = levelColor(latest.danger_level);
  const dc = latest.danger_level === "CRITICAL" ? "D" : latest.danger_level === "MEDIUM" ? "W" : "S";

  return (
    <div>
      <div className="hero">
        <div
          className="hero-chip"
          style={{
            background: latest.danger ? "rgba(239,68,68,.18)" : "rgba(34,197,94,.14)",
            color:      latest.danger ? "#ef4444" : "#22c55e",
            border:     `1px solid ${latest.danger ? "rgba(239,68,68,.3)" : "rgba(34,197,94,.28)"}`,
          }}
        >
          {latest.danger ? "Critical Alert" : "All Clear"}
        </div>

        <div className="hero-sensor-lbl">⚠️ Carbon Monoxide (CO)</div>

        <div className="hero-val" style={{ color: lc }}>
          {latest.sensors?.mq7 ?? "--"}<span className="hero-unit"> ppm</span>
        </div>

        <div className="hero-sum">{latest.summary}</div>
        <div className="hero-time">
          Recorded:{" "}
          {new Date(latest.timestamp).toLocaleString("en-US", {
            month: "short", day: "numeric",
            hour: "2-digit", minute: "2-digit",
          })}
        </div>

        <div style={{ marginTop: 20, background: "rgba(255,255,255,.03)", border: "1px solid var(--border)", borderRadius: 12, padding: "20px 20px 6px" }}>
          <div className="icard-title">Complete Info</div>

          <div className="iblock">
            <div className="iico blue">ℹ️</div>
            <div>
              <div className="ilbl">Summary &amp; Risks</div>
              <div className="itxt">
                Danger:{" "}
                <span className={`cc ${dc}`}>{latest.danger_level}</span>.{" "}
                {latest.summary}
              </div>
            </div>
          </div>

          {latest.actions.length > 0 && (
            <div className="iblock">
              <div className="iico green">🛡️</div>
              <div>
                <div className="ilbl">Recommended Action</div>
                <div className="itxt">
                  Immediate action:{" "}
                  <span className="cg">{latest.actions[0]}</span>.{" "}
                  {latest.actions.slice(1).join(". ")}
                </div>
              </div>
            </div>
          )}

          <div className="exp-row">
            <button className="exp-btn">⬇ Export Log</button>
          </div>
        </div>
      </div>

      <div className="sechdr">
        <div className="sec-title">Previous Scans</div>
      </div>

      <div className="slist">
        {history.slice(1).map(h => {
          const ic  = h.danger_level === "CRITICAL" ? "D" : h.danger_level === "MEDIUM" ? "W" : "S";
          const emo = h.danger_level === "CRITICAL" ? "🚨" : h.danger_level === "MEDIUM" ? "⚠️" : "✅";
          return (
            <div className="scan" key={h.id} onClick={() => onSelect(h)}>
              <div className={`scan-ico ${ic}`}>{emo}</div>
              <div className="scan-body">
                <div
                  className="scan-ttl"
                  style={{ color: h.danger ? levelColor(h.danger_level) : "var(--text)" }}
                >
                  {h.summary}
                </div>
                <div className="scan-sub">
                  {h.suspected_gas !== "None" ? h.suspected_gas : `CO: ${h.sensors?.mq7 ?? "--"} ppm`}
                </div>
              </div>
              <div className="scan-right">
                <div className="scan-time">{formatTime(h.timestamp)}</div>
                <div className="chev">›</div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="arc-link">View Archives (2024-Q3)</div>
    </div>
  );
}
