import type { LogEntry, Sensors } from "../types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export type AlarmScenario = "LIVE" | "SAFE" | "WARM" | "SMOKE" | "GAS_LEAK" | "FIRE_TEST";

interface ApiAnalysis {
  danger: boolean;
  danger_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  suspected_gas: string;
  confidence: number;
  summary: string;
  reasons: string[];
  actions: string[];
  trigger_buzzer: boolean;
  trigger_led: boolean;
}

interface ApiReadingPayload {
  _id?: string;
  device_id?: string;
  mq7: number;
  mq135: number;
  mq2: number;
  dht22_temp: number;
  dht22_humidity: number;
  flame_value?: number;
  flame_detected: boolean;
  timestamp?: string;
  created_at?: string;
  analysis: ApiAnalysis;
}

export interface ApiAlarmState {
  is_active: boolean;
  feed_paused: boolean;
  scenario: AlarmScenario;
  reading: Omit<ApiReadingPayload, "analysis"> | null;
  analysis: ApiAnalysis | null;
}

interface ApiLatestResponse {
  reading: Omit<ApiReadingPayload, "analysis"> | null;
  analysis: ApiAnalysis | null;
}

const apiFetch = async <T>(path: string): Promise<T> => {
  const response = await fetch(`${BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

function toLogEntry(payload: ApiReadingPayload): LogEntry {
  const timestamp = payload.timestamp || payload.created_at || new Date().toISOString();
  const sensors: Sensors = {
    mq7: payload.mq7,
    mq135: payload.mq135,
    mq2: payload.mq2,
    temp: payload.dht22_temp,
    humidity: payload.dht22_humidity,
    flame: payload.flame_detected,
  };

  return {
    id: payload._id ?? "latest",
    timestamp: typeof timestamp === "string" ? timestamp : new Date(timestamp).toISOString(),
    danger: payload.analysis.danger,
    danger_level: payload.analysis.danger_level,
    suspected_gas: payload.analysis.suspected_gas,
    confidence: payload.analysis.confidence,
    summary: payload.analysis.summary,
    reasons: payload.analysis.reasons,
    actions: payload.analysis.actions,
    trigger_buzzer: payload.analysis.trigger_buzzer,
    trigger_led: payload.analysis.trigger_led,
    sensors,
  };
}

export function alarmStateToLogEntry(state: ApiAlarmState): LogEntry | null {
  if (!state.reading || !state.analysis) {
    return null;
  }

  return toLogEntry({
    ...state.reading,
    analysis: state.analysis,
  });
}

export async function fetchLatestAnalysis(): Promise<LogEntry> {
  const data = await apiFetch<ApiLatestResponse>("/api/latest");
  
  // If no analysis available, throw error so fallback to mock data
  if (!data || !data.analysis) {
    throw new Error("No latest analysis available from backend");
  }

  const readingPayload: ApiReadingPayload = {
    mq7: data.reading?.mq7 ?? 0,
    mq135: data.reading?.mq135 ?? 0,
    mq2: data.reading?.mq2 ?? 0,
    dht22_temp: data.reading?.dht22_temp ?? 0,
    dht22_humidity: data.reading?.dht22_humidity ?? 0,
    flame_detected: data.reading?.flame_detected ?? false,
    timestamp: data.reading?.timestamp ?? new Date().toISOString(),
    analysis: data.analysis,
  };

  return toLogEntry(readingPayload);
}

export async function fetchAlarmState(): Promise<ApiAlarmState> {
  return apiFetch<ApiAlarmState>("/api/alarm");
}

export async function updateAlarmState(state: Partial<ApiAlarmState>): Promise<ApiAlarmState> {
  const response = await fetch(`${BASE_URL}/api/alarm`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(state),
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export async function fetchHistory(limit = 10): Promise<LogEntry[]> {
  const docs = await apiFetch<ApiReadingPayload[]>(`/api/readings?limit=${limit}`);
  return docs.map(toLogEntry);
}
