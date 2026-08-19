import { useForm } from "react-hook-form";
import { toast } from "sonner";
import PageHeader from "@/components/PageHeader";
import { Card, CardContent, CardHeader } from "@/components/ui/Card";

export default function FeaturePage() {
  const { register, handleSubmit, reset } = useForm({ defaultValues: { title: "", description: "" } });
  const onSubmit = (values) => { console.log(values); toast.success("Form submitted — connect this handler to your API."); reset(); };
  return <div className="container-app py-8"><PageHeader eyebrow="Feature template" title="CRUD-ready feature page" description="Use this as a starting point for events, communities, campaigns, volunteers, tasks, feedback, products, bookings, or any other domain." />
    <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
      <Card><CardHeader><h2 className="font-semibold">Create item</h2><p className="mt-1 text-sm text-slate-500">Replace fields based on your DB schema and API contract.</p></CardHeader><CardContent><form className="space-y-4" onSubmit={handleSubmit(onSubmit)}><div><label className="mb-1.5 block text-sm font-medium">Title</label><input className="input" placeholder="Example title" {...register("title", { required: true })} /></div><div><label className="mb-1.5 block text-sm font-medium">Description</label><textarea className="min-h-32 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-200" placeholder="Add useful context" {...register("description")} /></div><button className="btn-primary" type="submit">Save item</button></form></CardContent></Card>
      <Card><CardHeader><h2 className="font-semibold">API contract starter</h2><p className="mt-1 text-sm text-slate-500">Agree this with the backend teammate before integration.</p></CardHeader><CardContent><pre className="overflow-auto rounded-2xl bg-slate-950 p-4 text-xs leading-6 text-slate-300">{`GET    /items\nGET    /items/:id\nPOST   /items\nPUT    /items/:id\nDELETE /items/:id\n\nPOST /auth/login\nGET  /auth/me`}</pre></CardContent></Card>
    </div>
  </div>;
}
