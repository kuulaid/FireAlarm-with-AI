// Format timestamp to relative time or formatted date
export function formatTime(iso) {
  const d = new Date(iso);
  const diff = Date.now() - d;
  if (diff < 60000) return "Just now";
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" }) +
    " · " + d.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });
}

// Get color based on danger level
export function levelColor(level) {
  if (level === "CRITICAL") return "#ef4444";
  if (level === "MEDIUM")   return "#f97316";
  return "#22c55e";
}

// Get sensor status based on thresholds
export function getSensorStatus(val, warnAt, critAt) {
  if (val >= critAt) return "CRITICAL";
  if (val >= warnAt) return "WARNING";
  return "NORMAL";
}
