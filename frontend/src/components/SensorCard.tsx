import type { ReactNode } from "react";

interface SensorCardProps {
  children: ReactNode;
  className?: string;
}

// Simple card wrapper used for the sensor grid and detail cards.
export function SensorCard({ children, className = "" }: SensorCardProps) {
  return (
    <div className={`bg-slate-100 rounded-2xl p-4 border border-slate-200 hover-lift anim-item ${className}`}>
      {children}
    </div>
  );
}
