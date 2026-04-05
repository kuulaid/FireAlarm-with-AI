import { Activity, Droplets, Flame, Thermometer, Wind } from "lucide-react";
import { SensorStatus } from "../types";
import { getSensorStatus } from "../utils/format";
import { getSensorTheme } from "../utils/theme";
import { Chip } from "./Chip";
import { SensorCard } from "./SensorCard";
import { SensorIconBadge } from "./SensorIconBadge";

interface SensorGridProps {
  sensors: {
    mq7: number;
    mq135: number;
    mq2: number;
    temp: number;
    humidity: number;
    flame: boolean;
  };
}

// Displays the live sensor cards on the dashboard.
export function SensorGrid({ sensors }: SensorGridProps) {
  const { mq7, mq135, mq2, temp, humidity, flame } = sensors;
  const mq7Status = getSensorStatus(mq7, 70, 200);
  const mq135Status = getSensorStatus(mq135, 80, 120);
  const mq2Status = getSensorStatus(mq2, 100, 300);

  const mq7Theme = getSensorTheme(mq7Status);
  const mq135Theme = getSensorTheme(mq135Status);
  const mq2Theme = getSensorTheme(mq2Status);

  return (
    <div className="grid grid-cols-2 gap-3 mb-6">
      <SensorCard className="col-span-2">
        <div className="flex items-start justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <SensorIconBadge icon={<Wind className="w-4 h-4" />} status={mq7Status} />
            <div>
              <p className="text-[11px] text-slate-400 font-medium tracking-wide">MQ-7 Sensor</p>
              <p className="text-sm font-semibold text-slate-700">Carbon Monoxide</p>
            </div>
          </div>
          <Chip status={mq7Status} />
        </div>
        <div className="flex items-baseline gap-1">
          <span className={`font-extrabold text-5xl leading-none tracking-tight ${mq7Theme.text}`}>{mq7}</span>
          <span className="text-sm text-slate-400 font-normal">ppm</span>
        </div>
      </SensorCard>

      <SensorCard>
        <div className="flex items-start justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <SensorIconBadge icon={<Activity className="w-4 h-4" />} status={mq135Status} />
            <div>
              <p className="text-[11px] text-slate-400 font-medium tracking-wide">MQ-135</p>
              <p className="text-sm font-semibold text-slate-700">Air Quality</p>
            </div>
          </div>
          <Chip status={mq135Status} />
        </div>
        <div className="flex items-baseline gap-1">
          <span className={`font-extrabold text-4xl leading-none tracking-tight ${mq135Theme.text}`}>{mq135}</span>
          <span className="text-xs text-slate-400">ppm</span>
        </div>
      </SensorCard>

      <SensorCard>
        <div className="flex items-start justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <SensorIconBadge icon={<Flame className="w-4 h-4" />} status={mq2Status} />
            <div>
              <p className="text-[11px] text-slate-400 font-medium tracking-wide">MQ-2</p>
              <p className="text-sm font-semibold text-slate-700">Combustibles</p>
            </div>
          </div>
          <Chip status={mq2Status} />
        </div>
        <div className="flex items-baseline gap-1">
          <span className={`font-extrabold text-4xl leading-none tracking-tight ${mq2Theme.text}`}>{mq2}</span>
          <span className="text-xs text-slate-400">ppm</span>
        </div>
      </SensorCard>

      <SensorCard>
        <div className="flex items-center gap-2 mb-3">
          <div className="w-8 h-8 rounded-lg bg-slate-200 flex items-center justify-center flex-shrink-0">
            <Thermometer className="w-4 h-4 text-slate-500" />
          </div>
          <div>
            <p className="text-[11px] text-slate-400 font-medium tracking-wide">DHT22</p>
            <p className="text-sm font-semibold text-slate-700">Environment</p>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="flex items-center gap-1.5">
            <Thermometer className="w-3.5 h-3.5 text-orange-400 flex-shrink-0" />
            <span className="font-extrabold text-2xl text-slate-800 leading-none">{temp}</span>
            <span className="text-xs text-slate-400">°C</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Droplets className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
            <span className="font-extrabold text-2xl text-slate-800 leading-none">{humidity}</span>
            <span className="text-xs text-slate-400">%</span>
          </div>
        </div>
      </SensorCard>

      <SensorCard>
        <div className="flex items-center gap-2 mb-3">
          <div className="w-8 h-8 rounded-lg bg-slate-200 flex items-center justify-center flex-shrink-0">
            <Flame className="w-4 h-4 text-slate-500" />
          </div>
          <div>
            <p className="text-[11px] text-slate-400 font-medium tracking-wide">Flame Sensor (IR)</p>
            <p className="text-sm font-semibold text-slate-700">Fire Detection</p>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <Flame className={`w-7 h-7 ${flame ? "text-red-500 anim-wobble" : "text-slate-300"}`} />
          <p className={`text-sm font-semibold leading-snug ${flame ? "text-red-500" : "text-teal-600"}`}>
            {flame ? "Flame Detected!" : "No Flame Detected"}
          </p>
          <Chip status={flame ? "DANGER" : "SAFE"} />
        </div>
      </SensorCard>
    </div>
  );
}
