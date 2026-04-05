import { Menu } from "lucide-react";
import { PageKey } from "../types";

interface TopbarProps {
  page: PageKey;
  onToggleSidebar: () => void;
}

// Header bar shown at the top of the content area.
export function Topbar({ page, onToggleSidebar }: TopbarProps) {
  const titles: Record<PageKey, string> = {
    home: "Dashboard",
    history: "Detection History",
    detail: "Log Detail",
  };

  return (
    <header className="sticky top-0 z-[100] h-16 bg-slate-900 border-b border-white/5 flex items-center justify-between px-4 md:px-7 flex-shrink-0">
      <div className="flex items-center gap-3 min-w-0 flex-1">
        <button
          className="md:hidden btn-press flex-shrink-0 w-9 h-9 rounded-lg border border-white/10 text-white flex items-center justify-center"
          onClick={onToggleSidebar}
        >
          <Menu className="w-4 h-4" />
        </button>
        <div className="min-w-0">
          <p className="font-bold text-white text-base leading-tight truncate">{titles[page]}</p>
          <p className="text-[11px] text-slate-400">Environmental Monitoring</p>
        </div>
      </div>

      <div className="flex-shrink-0 flex items-center gap-1.5 bg-teal-500/10 border border-teal-500/30 text-teal-400 text-[11px] font-bold tracking-widest uppercase px-3 py-1.5 rounded-full">
        <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-pulse" />
        LIVE
      </div>
    </header>
  );
}
