import React, { useEffect, useRef, useState } from "react";
import { AlarmScenario, alarmStateToLogEntry, fetchAlarmState, updateAlarmState } from "../services/api";
import type { LogEntry } from "../types";

const SCENARIOS: Array<{
  key: AlarmScenario;
  title: string;
  description: string;
}> = [
  {
    key: "SAFE",
    title: "Safe Baseline",
    description: "Stable room scan near 26°C with no flame or gas spike.",
  },
  {
    key: "WARM",
    title: "Warm Room",
    description: "Higher ambient heat, but still below an alarm condition.",
  },
  {
    key: "PARTIAL_SMOKE",
    title: "Early Smoke",
    description: "Early stage smoke detection below critical threshold.",
  },
  {
    key: "SMOKE",
    title: "Smoke Test",
    description: "Elevated combustion readings without a flame confirmation.",
  },
  {
    key: "CO_DETECTION",
    title: "CO Leak",
    description: "Carbon monoxide detection - potential appliance malfunction.",
  },
  {
    key: "GAS_LEAK",
    title: "Gas Leak",
    description: "Critical combustible gas scenario without an open flame.",
  },
  {
    key: "EXTREME_HEAT",
    title: "Extreme Heat",
    description: "Extreme temperature spike - possible radiant fire.",
  },
  {
    key: "ELECTRICAL_FIRE",
    title: "Electrical Fire",
    description: "Rapid heat buildup with moderate gas - electrical origin.",
  },
  {
    key: "HIGH_HUMIDITY",
    title: "High Humidity",
    description: "Elevated moisture conditions - possible water leak.",
  },
  {
    key: "MIXED_HAZARD",
    title: "Mixed Hazard",
    description: "Multiple gas types and heat elevation detected.",
  },
  {
    key: "CONTROLLED_BURN",
    title: "Controlled Burn",
    description: "Low-intensity flame detected with moderate gas readings.",
  },
  {
    key: "DUSTY_AIR",
    title: "Dusty Air",
    description: "High particulate matter or dust in the air.",
  },
  {
    key: "FIRE_TEST",
    title: "Fire Test",
    description: "Direct flame placement with a critical alarm response.",
  },
];

const formatReading = (value: number | undefined | null) => (value == null ? "--" : value.toFixed(0));

const ManualAlarmSwitch: React.FC = () => {
  const [alarmState, setAlarmState] = useState<Awaited<ReturnType<typeof fetchAlarmState>> | null>(null);
  const [preview, setPreview] = useState<LogEntry | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const isSavingRef = useRef(false);

  const refreshState = async () => {
    if (isSavingRef.current) {
      return;
    }

    try {
      const state = await fetchAlarmState();
      setAlarmState(state);
      setPreview(alarmStateToLogEntry(state));
    } catch (error) {
      console.error("Failed to fetch alarm state:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshState();
    const intervalId = setInterval(refreshState, 2000);
    return () => clearInterval(intervalId);
  }, []);

  const applyUpdate = async (patch: Parameters<typeof updateAlarmState>[0]) => {
    if (isSaving) {
      return;
    }

    setIsSaving(true);
    isSavingRef.current = true;

    try {
      const nextState = await updateAlarmState(patch);
      setAlarmState(nextState);
      setPreview(alarmStateToLogEntry(nextState));
    } catch (error) {
      console.error("Failed to update alarm state:", error);
    } finally {
      setIsSaving(false);
      setTimeout(() => {
        isSavingRef.current = false;
      }, 300);
    }
  };

  const toggleFeedPause = async () => {
    await applyUpdate({ feed_paused: !(alarmState?.feed_paused ?? false) });
  };

  const turnBuzzerOn = async () => {
    await applyUpdate({ is_active: true });
  };

  const turnBuzzerOff = async () => {
    await applyUpdate({ is_active: false });
  };

  const selectScenario = async (scenario: AlarmScenario) => {
    await applyUpdate({ feed_paused: true, scenario });
  };

  const resumeLiveFeed = async () => {
    await applyUpdate({ feed_paused: false, scenario: "LIVE" });
  };

  if (isLoading) {
    return <div className="text-slate-400 text-center animate-pulse">Syncing with system...</div>;
  }

  const isPaused = alarmState?.feed_paused ?? false;

  return (
    <div className="w-full max-w-3xl rounded-3xl border border-slate-700 bg-slate-950/95 p-6 text-slate-100 shadow-2xl shadow-black/40">
      <div className="mb-6">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-slate-400">Alarm Control</p>
        <h2 className="mt-2 text-2xl font-bold text-white">Manual scan and buzzer override</h2>
        <p className="mt-2 max-w-2xl text-sm text-slate-400">
          Pause the live ESP32 feed, choose a realistic test scenario around the room's 26°C baseline, and toggle the buzzer independently.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <button
          onClick={toggleFeedPause}
          disabled={isSaving}
          className={`rounded-2xl border px-4 py-4 text-left transition-all ${
            isPaused
              ? "border-amber-400/50 bg-amber-500/10 text-amber-100"
              : "border-emerald-400/30 bg-emerald-500/10 text-emerald-100"
          } ${isSaving ? "opacity-60 cursor-not-allowed" : "hover:scale-[1.01]"}`}
        >
          <div className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">ESP32 Feed</div>
          <div className="mt-1 text-lg font-bold">{isPaused ? "Paused for manual scanning" : "Live feed active"}</div>
          <div className="mt-1 text-sm text-slate-300">
            {isPaused ? "The app will use the selected manual scan scenario." : "ESP32 readings continue to drive the dashboard."}
          </div>
        </button>

        <div className="rounded-2xl border border-slate-700 bg-slate-900/50 p-4">
          <div className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400 mb-3">Buzzer Control</div>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={turnBuzzerOn}
              disabled={isSaving}
              className={`rounded-lg border px-3 py-2 text-sm font-semibold transition-all ${
                alarmState?.is_active
                  ? "border-red-400 bg-red-500/15 text-red-200"
                  : "border-slate-600 bg-slate-800 text-slate-300 hover:border-red-400/50"
              } ${isSaving ? "opacity-60 cursor-not-allowed" : "hover:scale-[1.02]"}`}
            >
              Turn On
            </button>
            <button
              onClick={turnBuzzerOff}
              disabled={isSaving}
              className={`rounded-lg border px-3 py-2 text-sm font-semibold transition-all ${
                !alarmState?.is_active
                  ? "border-slate-500 bg-slate-800 text-slate-200"
                  : "border-slate-600 bg-slate-900 text-slate-300 hover:border-slate-500"
              } ${isSaving ? "opacity-60 cursor-not-allowed" : "hover:scale-[1.02]"}`}
            >
              Turn Off
            </button>
          </div>
          <div className="mt-2 text-sm text-slate-400">
            Current: <span className={alarmState?.is_active ? "text-red-200 font-semibold" : "text-slate-300"}>{alarmState?.is_active ? "On" : "Off"}</span>
          </div>
        </div>
      </div>

      <div className="mt-6">
        <div className="mb-3 flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Scan presets</p>
            <p className="mt-1 text-sm text-slate-400">Select one to pause live data and simulate a realistic environmental scan.</p>
          </div>
          <button
            onClick={resumeLiveFeed}
            disabled={isSaving}
            className="rounded-full border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:border-slate-500 hover:bg-slate-900 disabled:opacity-60"
          >
            Resume Live Feed
          </button>
        </div>

        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {SCENARIOS.map((scenario) => {
            const isSelected = alarmState?.scenario === scenario.key && isPaused;

            return (
              <button
                key={scenario.key}
                onClick={() => selectScenario(scenario.key)}
                disabled={isSaving}
                className={`rounded-2xl border p-4 text-left transition-all ${
                  isSelected
                    ? "border-cyan-400 bg-cyan-500/10 shadow-[0_0_0_1px_rgba(34,211,238,0.25)]"
                    : "border-slate-700 bg-slate-900/80 hover:border-slate-500 hover:bg-slate-900"
                } ${isSaving ? "opacity-60 cursor-not-allowed" : "hover:translate-y-[-1px]"}`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="text-base font-bold text-white">{scenario.title}</span>
                  {isSelected && <span className="rounded-full bg-cyan-400/15 px-2 py-1 text-[10px] font-bold uppercase tracking-[0.2em] text-cyan-200">Active</span>}
                </div>
                <p className="mt-2 text-sm leading-5 text-slate-400">{scenario.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">Current preview</p>
            <p className="mt-1 text-sm text-slate-300">
              {alarmState?.feed_paused ? `Scenario ${alarmState.scenario}` : "Live ESP32 feed enabled"}
            </p>
          </div>
          <div className={`rounded-full px-3 py-1 text-xs font-bold uppercase tracking-[0.2em] ${alarmState?.is_active ? "bg-red-500/15 text-red-200" : "bg-slate-800 text-slate-300"}`}>
            {alarmState?.is_active ? "Buzzer On" : "Buzzer Off"}
          </div>
        </div>

        {preview ? (
          <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-xl bg-slate-950/70 p-3">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Status</div>
              <div className="mt-1 text-lg font-semibold text-white">{preview.danger_level}</div>
              <div className="mt-1 text-sm text-slate-400">{preview.summary}</div>
            </div>
            <div className="rounded-xl bg-slate-950/70 p-3">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Temperature</div>
              <div className="mt-1 text-lg font-semibold text-white">{formatReading(alarmState?.reading?.dht22_temp)}°C</div>
              <div className="mt-1 text-sm text-slate-400">Baseline room temperature is 26°C.</div>
            </div>
            <div className="rounded-xl bg-slate-950/70 p-3">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-500">Flame</div>
              <div className="mt-1 text-lg font-semibold text-white">{alarmState?.reading?.flame_detected ? "Detected" : "Clear"}</div>
              <div className="mt-1 text-sm text-slate-400">Analog value: {formatReading(alarmState?.reading?.flame_value)}</div>
            </div>
          </div>
        ) : (
          <div className="mt-4 rounded-xl border border-dashed border-slate-700 px-4 py-6 text-sm text-slate-400">
            No simulated preview is active. Select a scenario to create one.
          </div>
        )}
      </div>
    </div>
  );
};

export default ManualAlarmSwitch;