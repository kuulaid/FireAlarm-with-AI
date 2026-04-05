import type { ReactNode } from "react";
import { PageKey } from "../types";

interface NavItem {
  key: string;
  pages: PageKey[];
  label: string;
  icon: ReactNode;
}

interface BottomNavProps {
  page: PageKey;
  navItems: NavItem[];
  onNavigate: (page: PageKey) => void;
}

// Mobile-friendly bottom navigation bar.
export function BottomNav({ page, navItems, onNavigate }: BottomNavProps) {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-slate-900 border-t border-white/5 z-[300] flex">
      {navItems.map(({ key, pages, label, icon }) => {
        const isActive = pages.includes(page);
        return (
          <button
            key={key}
            onClick={() => onNavigate(pages[0])}
            className={[
              "flex-1 flex flex-col items-center justify-center gap-1 text-[10px] font-bold tracking-widest uppercase transition-colors",
              isActive ? "text-blue-400" : "text-slate-500",
            ].join(" ")}
          >
            <span className="w-5 h-5 flex items-center justify-center">{icon}</span>
            {label}
          </button>
        );
      })}
    </nav>
  );
}
