import { Outlet, NavLink } from "react-router-dom";
import { Menu, Sparkles, X } from "lucide-react";
import { useState } from "react";

const nav = [
  { to: "/", label: "Home" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/feature", label: "Feature" },
];

export default function Layout() {
  const [open, setOpen] = useState(false);
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/90 backdrop-blur">
        <div className="container-app flex h-16 items-center justify-between">
          <NavLink to="/" className="flex items-center gap-2 font-semibold tracking-tight">
            <span className="grid size-9 place-items-center rounded-xl bg-slate-900 text-white"><Sparkles size={18} /></span>
            <span>{import.meta.env.VITE_APP_NAME || "Hackathon App"}</span>
          </NavLink>
          <nav className="hidden gap-1 md:flex">
            {nav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => `rounded-xl px-3 py-2 text-sm transition ${isActive ? "bg-slate-100 font-medium text-slate-900" : "text-slate-500 hover:bg-slate-100 hover:text-slate-900"}`}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          <button className="btn-ghost md:hidden" onClick={() => setOpen((v) => !v)} aria-label="Toggle navigation">
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        {open && (
          <div className="border-t border-slate-200 bg-white px-4 py-3 md:hidden">
            <div className="container-app flex flex-col gap-1 px-0">
              {nav.map((item) => (
                <NavLink key={item.to} to={item.to} onClick={() => setOpen(false)} className="rounded-xl px-3 py-2 text-sm hover:bg-slate-100">
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>
        )}
      </header>
      <main><Outlet /></main>
      <footer className="border-t border-slate-200 py-8">
        <div className="container-app text-xs text-slate-500">Built for rapid hackathon prototyping.</div>
      </footer>
    </div>
  );
}
