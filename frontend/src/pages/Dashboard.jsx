import { Activity, CheckCircle2, Clock3, Users } from "lucide-react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import PageHeader from "@/components/PageHeader";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";
import { MetricCard } from "@/components/ui/MetricCard";
import { StatusBadge } from "@/components/ui/StatusBadge";

const data = [
  { name: "Mon", value: 24 }, { name: "Tue", value: 31 }, { name: "Wed", value: 28 }, { name: "Thu", value: 42 }, { name: "Fri", value: 37 }, { name: "Sat", value: 51 }, { name: "Sun", value: 46 }
];

const rows = [
  { title: "Campaign Alpha", owner: "Team A", status: "success", label: "On track" },
  { title: "Volunteer Drive", owner: "Team B", status: "warning", label: "Needs attention" },
  { title: "Survey rollout", owner: "Team C", status: "info", label: "In progress" },
];

export default function Dashboard() {
  return <div className="container-app py-8"><PageHeader eyebrow="Starter dashboard" title="A reusable dashboard shell" description="Replace the sample metrics, chart data and table with your hackathon domain." actions={<button className="btn-primary">Primary action</button>} />
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <MetricCard icon={Users} label="Users / records" value="2,481" helper="Example KPI" trend="+12.4% this week" />
      <MetricCard icon={Activity} label="Active items" value="128" helper="Example KPI" trend="+8.2% this week" />
      <MetricCard icon={CheckCircle2} label="Completed" value="86%" helper="Example KPI" />
      <MetricCard icon={Clock3} label="At risk" value="14" helper="Example KPI" />
    </div>
    <div className="mt-4 grid gap-4 lg:grid-cols-[1.5fr_1fr]">
      <Card><CardHeader><h2 className="font-semibold">Activity / impact</h2><p className="mt-1 text-sm text-slate-500">Recharts is ready for your data.</p></CardHeader><CardContent><div className="h-72"><ResponsiveContainer width="100%" height="100%"><BarChart data={data}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="name" tickLine={false} axisLine={false} /><YAxis tickLine={false} axisLine={false} /><Tooltip /><Bar dataKey="value" radius={[8,8,0,0]} fill="#0f172a" /></BarChart></ResponsiveContainer></div></CardContent></Card>
      <Card><CardHeader><h2 className="font-semibold">Current priorities</h2><p className="mt-1 text-sm text-slate-500">Status-driven UI from the hackathon research.</p></CardHeader><CardContent><div className="space-y-3">{rows.map((r) => <div key={r.title} className="rounded-2xl border border-slate-200 p-4"><div className="flex items-center justify-between gap-3"><div><div className="font-medium">{r.title}</div><div className="mt-1 text-xs text-slate-500">Owner: {r.owner}</div></div><StatusBadge status={r.status}>{r.label}</StatusBadge></div></div>)}</div></CardContent></Card>
    </div>
  </div>;
}
