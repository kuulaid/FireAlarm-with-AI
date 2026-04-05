export default function AlertBanner({ data }) {
  const lvl   = data.danger_level;
  const label = data.danger ? `${lvl} Alert` : "All Systems Nominal";
  const title = data.danger
    ? (lvl === "CRITICAL" ? "Critical Atmosphere Warning" : "Elevated Gas Levels Detected")
    : "No Hazardous Conditions Detected";

  return (
    <div className={`alert ${lvl}`}>
      <div className="al-label">
        {data.danger ? "⚠️" : "✅"} {label}
      </div>
      <div className="al-title">{title}</div>
      {data.danger && data.actions.length > 0 ? (
        <div className="al-actions">
          <button className="al-btn prim">⚡ {data.actions[0]}</button>
          {data.actions[1] && (
            <button className="al-btn sec">🔍 {data.actions[1]}</button>
          )}
        </div>
      ) : (
        <div style={{ fontSize: 13, opacity: .8, marginTop: 2 }}>{data.summary}</div>
      )}
      <div className="al-deco">!</div>
    </div>
  );
}
