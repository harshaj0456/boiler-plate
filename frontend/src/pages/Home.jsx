import { ArrowRight, BarChart3, Database, Map, Smartphone, Sparkles, Zap } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";
import { useOnlineStatus } from "@/hooks/useOnlineStatus";

const features = [
  [Map, "Map-ready", "Plug in Leaflet, Google Maps or another provider only when the problem needs it."],
  [Sparkles, "AI-ready", "Add a chatbot, recommendations, summaries or RAG without reshaping the app."],
  [Database, "API-ready", "Axios + a clean API layer keeps React independent from backend implementation details."],
  [Smartphone, "PWA-ready", "Manifest and service-worker plumbing are included for app-like and offline scenarios."],
  [BarChart3, "Analytics-ready", "Recharts is available for KPIs, trends, impact and operational dashboards."],
  [Zap, "Fast to change", "Reusable cards, badges, states, forms and layouts help you move during a 12-hour build."],
];

export default function Home() {
  const online = useOnlineStatus();
  return (
    <div className="container-app py-12 sm:py-16">
      <motion.section initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="max-w-3xl">
        <div className="inline-flex items-center gap-2 rounded-full bg-slate-900 px-3 py-1 text-xs font-medium text-white"><span className={`size-1.5 rounded-full ${online ? "bg-emerald-400" : "bg-rose-400"}`} />{online ? "Online" : "Offline"}</div>
        <h1 className="mt-5 text-4xl font-semibold tracking-tight sm:text-6xl">Build the solution, not the setup.</h1>
        <p className="mt-5 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">A generic React + Vite + Tailwind starter for hackathons. Keep the shell, swap the domain, and connect it to your Python/Node backend.</p>
        <div className="mt-7 flex flex-wrap gap-3"><Link to="/dashboard" className="btn-primary"><span>Open demo dashboard</span><ArrowRight size={17} /></Link><Link to="/feature" className="btn-secondary">See feature template</Link></div>
      </motion.section>

      <section className="mt-14 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {features.map(([Icon, title, desc], index) => <motion.div key={title} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.05 }}><Card className="h-full p-5"><div className="grid size-10 place-items-center rounded-xl bg-slate-100"><Icon size={19} /></div><h2 className="mt-4 font-semibold">{title}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{desc}</p></Card></motion.div>)}
      </section>

      <section className="mt-14 rounded-3xl bg-slate-900 p-6 text-white sm:p-8">
        <div className="grid gap-8 lg:grid-cols-2 lg:items-center">
          <div><p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">Hackathon principle</p><h2 className="mt-2 text-2xl font-semibold">Understand the problem → define the data → agree the API → ship the MVP.</h2></div>
          <pre className="overflow-auto rounded-2xl bg-slate-950 p-5 text-xs leading-6 text-slate-300">{`React UI\n   ↓\nAPI contract\n   ↓\nBackend\n   ↓\nDatabase\n\nOptional layers:\nAI · Maps · PWA · Analytics`}</pre>
        </div>
      </section>
    </div>
  );
}
