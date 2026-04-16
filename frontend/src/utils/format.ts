import { SensorStatus } from "../types";

const DISPLAY_TIME_ZONE = "Asia/Manila";

export function formatDateTime(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleString("en-US", {
    timeZone: DISPLAY_TIME_ZONE,
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true,
  });
}

// Convert an ISO timestamp into a human-friendly label.
export function formatTime(iso: string): string {
  const date = new Date(iso);
  const diff = Date.now() - date.getTime();

  if (diff < 60_000) return "Just now";
  if (diff < 3_600_000) return `${Math.floor(diff / 60_000)}m ago`;
  if (diff < 86_400_000) return `${Math.floor(diff / 3_600_000)}h ago`;

  return (
    date.toLocaleDateString("en-US", { month: "short", day: "numeric", timeZone: DISPLAY_TIME_ZONE }) +
    " · " +
    date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", timeZone: DISPLAY_TIME_ZONE })
  );
}

// Determine sensor status based on warning and critical thresholds.
export function getSensorStatus(val: number, warnAt: number, critAt: number): SensorStatus {
  if (val >= critAt) return "CRITICAL";
  if (val >= warnAt) return "WARNING";
  return "NORMAL";
}
