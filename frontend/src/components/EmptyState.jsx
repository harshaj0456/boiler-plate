import { Inbox } from "lucide-react";
export default function EmptyState({ title = "Nothing here yet", description = "Add your first item to get started." }) {
  return <div className="card grid place-items-center p-10 text-center"><div className="grid size-12 place-items-center rounded-2xl bg-slate-100"><Inbox size={22} /></div><h3 className="mt-4 font-semibold">{title}</h3><p className="mt-1 max-w-md text-sm text-slate-500">{description}</p></div>;
}
