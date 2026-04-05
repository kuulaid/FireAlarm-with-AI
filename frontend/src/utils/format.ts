import { SensorStatus } from "../types";

// Convert an ISO timestamp into a human-friendly label.
export function formatTime(iso: string): string {
  const date = new Date(iso);
  const diff = Date.now() - date.getTime();

  if (diff < 60_000) return "Just now";
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)}m ago`;
  if (diff < 86_400_000) return `${Math.floor(diff / 3_600_000)}h ago`;

  return (
    date.toLocaleDateString("en-US", { month: "short", day: "numeric" }) +
    " · " +
    date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })
  );
}

// Determine sensor status based on warning and critical thresholds.
export function getSensorStatus(val: number, warnAt: number, critAt: number): SensorStatus {
  if (val >= critAt) return "CRITICAL";
  if (val >= warnAt) return "WARNING";
  return "NORMAL";
}
