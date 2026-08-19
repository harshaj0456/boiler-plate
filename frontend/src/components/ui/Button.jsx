import { cn } from "@/lib/utils";

export function Button({ variant = "primary", className, ...props }) {
  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    ghost: "btn-ghost",
  };
  return <button className={cn(variants[variant] || variants.primary, className)} {...props} />;
}
