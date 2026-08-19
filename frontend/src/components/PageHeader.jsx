export default function PageHeader({ eyebrow, title, description, actions }) {
  return <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><div className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">{eyebrow}</div><h1 className="mt-2 text-3xl font-semibold tracking-tight">{title}</h1>{description && <p className="mt-2 max-w-2xl text-sm text-slate-500">{description}</p>}</div>{actions}</div>;
}
