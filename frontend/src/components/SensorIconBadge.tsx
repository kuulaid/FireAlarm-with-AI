import { SensorStatus } from "../types";
import { getSensorTheme } from "../utils/theme";

import type { ReactNode } from "react";

interface SensorIconBadgeProps {
  icon: ReactNode;
  status: SensorStatus;
}

// Shows a rounded badge with the correct tint and wobble animation for critical sensor readings.
export function SensorIconBadge({ icon, status }: SensorIconBadgeProps) {
  const theme = getSensorTheme(status);

  return (
    <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 transition-colors duration-300 ${theme.iconBg}`}>
      <span className={`transition-colors duration-300 ${theme.iconText} ${theme.wobble ? "anim-wobble" : ""}`}>
        {icon}
      </span>
    </div>
  );
}
