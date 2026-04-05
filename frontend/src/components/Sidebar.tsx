import type { ReactNode } from "react";
import { Factory, User } from "lucide-react";
import { PageKey } from "../types";

interface NavItem {
  key: string;
  pages: PageKey[];
  label: string;
  icon: ReactNode;
}

interface SidebarProps {
  page: PageKey;
  navItems: NavItem[];
  onNavigate: (page: PageKey) => void;
  open: boolean;
}

// Side navigation panel for desktop and mobile views.
export function Sidebar({ page, navItems, onNavigate, open }: SidebarProps) {
  return (
    <nav
      className={[
        "fixed top-0 left-0 bottom-0 z-[200] w-60 bg-slate-900 border-r border-white/5",
        "flex flex-col px-3.5 py-6 transition-transform duration-300 ease-in-out",
        open ? "translate-x-0 shadow-2xl" : "-translate-x-full",
        "md:translate-x-0",
      ].join(" ")}
    >
      <div className="flex items-center gap-2.5 px-2 mb-8">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center flex-shrink-0">
          <Factory className="w-5 h-5 text-white" />
        </div>
        <div className="text-[11px] font-black tracking-widest uppercase text-white leading-snug">
          Industrial
          <br />
          Precision
        </div>
      </div>

      <div className="flex-1 flex flex-col gap-1">
        {navItems.map(({ key, pages, label, icon }) => {
          const isActive = pages.includes(page);
          return (
            <button
              key={key}
              onClick={() => onNavigate(pages[0])}
              className={[
                "btn-press flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-left transition-colors",
                isActive
                  ? "bg-blue-500/10 text-blue-400"
                  : "text-slate-400 hover:bg-white/5 hover:text-white",
              ].join(" ")}
            >
              <span className="w-5 flex items-center justify-center flex-shrink-0">{icon}</span>
              {label}
            </button>
          );
        })}
      </div>

      <div className="border-t border-white/5 pt-4 flex items-center gap-2.5 pl-1">
        <div className="w-8 h-8 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center justify-center flex-shrink-0">
          <User className="w-4 h-4 text-blue-400" />
        </div>
        <div>
          <p className="text-sm font-semibold text-white">Admin</p>
          <p className="text-[11px] text-slate-500">Safety Officer</p>
        </div>
      </div>
    </nav>
  );
}
