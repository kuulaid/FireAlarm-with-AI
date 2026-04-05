export type DangerLevel = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
export type SensorStatus = "CRITICAL" | "WARNING" | "NORMAL";
export type ChipStatus = SensorStatus | "SAFE" | "DANGER";
export type PageKey = "home" | "history" | "detail";

export interface Sensors {
  mq7: number;
  mq135: number;
  mq2: number;
  temp: number;
  humidity: number;
  flame: boolean;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  danger: boolean;
  danger_level: DangerLevel;
  suspected_gas: string;
  confidence: number;
  summary: string;
  reasons: string[];
  actions: string[];
  trigger_buzzer: boolean;
  trigger_led: boolean;
  sensors: Sensors;
}
