import { levelColor } from "../utils/helpers";

export default function DetailPage({ log, onBack }) {
  const s   = log.sensors || {};
  const lvl = log.danger_level;
  const dc  = lvl === "CRITICAL" ? "D" : lvl === "MEDIUM" ? "W" : "S";

  return (
    <div>
      <button className="back-btn" onClick={onBack}>← Back to History</button>

      <div
        className="hero"
        style={{
          background:  log.danger ? "linear-gradient(135deg,#1a0808,#2d1010)" : "var(--surf)",
          borderColor: log.danger ? "rgba(239,68,68,.22)" : "var(--border)",
        }}
      >
        <div
          className="hero-chip"
          style={{
            background: log.danger ? "rgba(239,68,68,.18)" : "rgba(34,197,94,.14)",
            color:      log.danger ? "#ef4444" : "#22c55e",
            border:     `1px solid ${log.danger ? "rgba(239,68,68,.3)" : "rgba(34,197,94,.28)"}`,
          }}
        >
          {lvl}
        </div>

        <div className="hero-sensor-lbl">🗓 {new Date(log.timestamp).toLocaleString()}</div>

        <div className="hero-val" style={{ color: levelColor(lvl), fontSize: "clamp(36px,6vw,52px)" }}>
          {s.mq7 ?? "--"}<span className="hero-unit"> ppm CO</span>
        </div>

        <div className="hero-sum">{log.summary}</div>

        {log.suspected_gas !== "None" && (
          <div style={{ marginTop: 8, fontSize: 13, color: "var(--muted)" }}>
            Suspected: <span style={{ color: levelColor(lvl), fontWeight: 600 }}>{log.suspected_gas}</span>
            {" "}· Confidence: {log.confidence}%
          </div>
        )}
      </div>

      <div className="icard">
        <div className="icard-title">Sensor Snapshot</div>
        <div className="snap-grid">
          {[
            { l: "MQ-7 CO",     v: s.mq7,      u: "ppm", flame: false },
            { l: "MQ-135 AQ",   v: s.mq135,    u: "ppm", flame: false },
            { l: "MQ-2 Comb.",  v: s.mq2,      u: "ppm", flame: false },
            { l: "Temperature", v: s.temp,     u: "°C",  flame: false },
            { l: "Humidity",    v: s.humidity, u: "%",   flame: false },
            { l: "Flame",       v: s.flame ? "YES" : "NO", u: "", flame: true },
          ].map(({ l, v, u, flame }) => (
            <div className="snap-cell" key={l}>
              <div className="snap-lbl">{l}</div>
              <div
                className="snap-val"
                style={{ color: flame ? (v === "YES" ? "#ef4444" : "#22c55e") : "var(--text)" }}
              >
                {v}<span className="snap-unit">{u}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="icard">
        <div className="icard-title">Complete Analysis</div>

        <div className="iblock">
          <div className="iico blue">ℹ️</div>
          <div>
            <div className="ilbl">Summary &amp; Risks</div>
            <div className="itxt">
              Danger level: <span className={`cc ${dc}`}>{lvl}</span>. {log.summary}
            </div>
          </div>
        </div>

        {log.actions.length > 0 && (
          <div className="iblock">
            <div className="iico green">🛡️</div>
            <div>
              <div className="ilbl">Recommended Actions</div>
              <ul className="rlist">
                {log.actions.map((a, i) => <li key={i}>{a}</li>)}
              </ul>
            </div>
          </div>
        )}

        <div className="iblock">
          <div className="iico blue">📋</div>
          <div>
            <div className="ilbl">Analysis Reasons</div>
            <ul className="rlist">
              {log.reasons.map((r, i) => <li key={i}>{r}</li>)}
            </ul>
          </div>
        </div>

        <div className="exp-row">
          <button className="exp-btn">⬇ Export Log</button>
        </div>
      </div>
    </div>
  );
}
