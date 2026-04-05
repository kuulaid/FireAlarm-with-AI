import { ChipStatus, DangerLevel, SensorStatus } from "../types";

export interface LevelTheme {
  textStrong: string;
  textMuted: string;
  bgSoft: string;
  bgMedium: string;
  bgGradient: string;
  border: string;
  iconColor: string;
  chipClass: string;
  bannerExtra: string;
  pillClass: string;
}

export interface SensorTheme {
  text: string;
  chip: string;
  iconBg: string;
  iconText: string;
  wobble: boolean;
}

// Map danger levels to shared theme tokens used by multiple components.
export function getLevelTheme(lvl: DangerLevel): LevelTheme {
  switch (lvl) {
    case "CRITICAL":
    case "HIGH":
      return {
        textStrong: "text-red-500",
        textMuted: "text-red-400",
        bgSoft: "bg-red-50",
        bgMedium: "bg-red-100",
        bgGradient: "bg-gradient-to-br from-red-700 to-red-800",
        border: "border-red-200",
        iconColor: "text-red-500",
        chipClass: "bg-red-100 text-red-600 border border-red-200",
        bannerExtra: "anim-critical-glow",
        pillClass: "bg-red-50 text-red-500 border border-red-200",
      };
    case "MEDIUM":
      return {
        textStrong: "text-orange-500",
        textMuted: "text-orange-400",
        bgSoft: "bg-orange-50",
        bgMedium: "bg-orange-100",
        bgGradient: "bg-gradient-to-br from-orange-600 to-orange-700",
        border: "border-orange-200",
        iconColor: "text-orange-500",
        chipClass: "bg-orange-100 text-orange-500 border border-orange-200",
        bannerExtra: "anim-medium-glow",
        pillClass: "bg-orange-50 text-orange-500 border border-orange-200",
      };
    default:
      return {
        textStrong: "text-teal-600",
        textMuted: "text-teal-500",
        bgSoft: "bg-teal-50",
        bgMedium: "bg-teal-100",
        bgGradient: "bg-gradient-to-br from-teal-600 to-teal-700",
        border: "border-teal-200",
        iconColor: "text-teal-500",
        chipClass: "bg-teal-50 text-teal-600 border border-teal-200",
        bannerExtra: "",
        pillClass: "bg-teal-50 text-teal-600 border border-teal-200",
      };
  }
}

// Map individual sensor status to visual tokens used throughout the sensor grid.
export function getSensorTheme(s: SensorStatus): SensorTheme {
  switch (s) {
    case "CRITICAL":
      return {
        text: "text-red-500",
        chip: "bg-red-100 text-red-600 border border-red-200",
        iconBg: "bg-red-100",
        iconText: "text-red-500",
        wobble: true,
      };
    case "WARNING":
      return {
        text: "text-orange-500",
        chip: "bg-orange-100 text-orange-500 border border-orange-200",
        iconBg: "bg-orange-50",
        iconText: "text-orange-500",
        wobble: false,
      };
    default:
      return {
        text: "text-slate-800",
        chip: "bg-blue-50 text-blue-500 border border-blue-100",
        iconBg: "bg-slate-200",
        iconText: "text-slate-500",
        wobble: false,
      };
  }
}

export function getChipClass(status: ChipStatus): string {
  if (status === "SAFE") return "bg-teal-50 text-teal-600 border border-teal-200";
  if (status === "DANGER") return "bg-red-100 text-red-600 border border-red-200";
  return getSensorTheme(status as SensorStatus).chip;
}
