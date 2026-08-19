import { Card } from "./Card";

export function MetricCard({ icon: Icon, label, value, helper, trend }) {
  return (
    <Card className="p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-slate-500">{label}</p>
          <p className="mt-2 text-3xl font-semibold tracking-tight">{value}</p>
          <p className="mt-1 text-xs text-slate-500">{helper}</p>
        </div>
        {Icon && <div className="grid size-10 place-items-center rounded-xl bg-slate-100"><Icon size={19} /></div>}
      </div>
      {trend && <div className="mt-4 text-xs font-medium text-emerald-600">{trend}</div>}
    </Card>
  );
}
