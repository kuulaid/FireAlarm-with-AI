import type { ReactNode } from "react";

interface InfoBlockProps {
  icon: ReactNode;
  iconBg: string;
  label: string;
  children: ReactNode;
  noBorder?: boolean;
}

// Reusable info row with a leading icon, title, and body content.
export function InfoBlock({ icon, iconBg, label, children, noBorder = false }: InfoBlockProps) {
  return (
    <div className={`flex gap-3 py-4 ${noBorder ? "" : "border-b border-slate-200"}`}>
      <div className={`w-9 h-9 rounded-xl ${iconBg} flex items-center justify-center flex-shrink-0`}>
        {icon}
      </div>
      <div className="min-w-0">
        <p className="text-[10px] font-bold tracking-widest uppercase text-slate-400 mb-1">{label}</p>
        {children}
      </div>
    </div>
  );
}
