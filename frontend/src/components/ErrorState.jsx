import { AlertTriangle } from "lucide-react";
export default function ErrorState({ title = "Something went wrong", description = "Check the API or try again.", onRetry }) {
  return <div className="card p-8 text-center"><div className="mx-auto grid size-12 place-items-center rounded-2xl bg-rose-50 text-rose-600"><AlertTriangle size={22} /></div><h3 className="mt-4 font-semibold">{title}</h3><p className="mt-1 text-sm text-slate-500">{description}</p>{onRetry && <button className="btn-secondary mt-5" onClick={onRetry}>Try again</button>}</div>;
}
