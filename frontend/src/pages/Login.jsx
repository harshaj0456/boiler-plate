import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { authApi, setAccessToken } from "@/api/auth";

const LOGIN_CONFIG = {
  brand: import.meta.env.VITE_APP_NAME || "Your App",
  eyebrow: import.meta.env.VITE_APP_EYEBROW || "Hackathon Solution",
  subheading:
    import.meta.env.VITE_APP_TAGLINE ||
    "Technology that turns ideas into measurable impact.",

  roles: [
    {
      id: "user",
      label: "User",
      description: "Access your workspace and features",
    },
    {
      id: "admin",
      label: "Admin",
      description: "Manage the platform and monitor activity",
    },
  ],

  story: {
    kicker: "Your Problem · Your Solution",
    taglines: ["Think Bigger.", "Build Better.", "Create Impact.", "Move Forward."],
    purposeTitle: "Our Purpose",
    purpose:
      "Replace this with the problem your team is solving and why it matters.",
    impactTitle: "Our Impact",
    impact:
      "Replace this with the measurable outcome your solution is designed to create.",
    stats: [
      { value: "01", label: "Core problem" },
      { value: "03", label: "Priority features" },
      { value: "∞", label: "Room to scale" },
    ],
  },
};

const SLIDES = [
  {
    src: "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1400&q=80",
    alt: "Team collaborating around a table",
  },
  {
    src: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1400&q=80",
    alt: "Person working on a laptop",
  },
  {
    src: "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1400&q=80",
    alt: "People collaborating in a modern workspace",
  },
  {
    src: "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1400&q=80",
    alt: "Team discussing ideas",
  },
];

export default function Login() {
  const navigate = useNavigate();

  const [slide, setSlide] = useState(0);
  const [tagline, setTagline] = useState(0);
  const [role, setRole] = useState("user");
  const [mode, setMode] = useState("login");
  const [face, setFace] = useState("purpose");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const next = useCallback(() => {
    setSlide((current) => (current + 1) % SLIDES.length);
  }, []);

  const prev = useCallback(() => {
    setSlide(
      (current) => (current - 1 + SLIDES.length) % SLIDES.length,
    );
  }, []);

  useEffect(() => {
    const id = setInterval(next, 4800);
    return () => clearInterval(id);
  }, [next]);

  useEffect(() => {
    const id = setInterval(() => {
      setTagline(
        (current) =>
          (current + 1) % LOGIN_CONFIG.story.taglines.length,
      );
    }, 3200);

    return () => clearInterval(id);
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);

      if (mode === "register") {
        if (!name.trim()) {
          setError("Please enter your name.");
          return;
        }

        const response = await authApi.register({
          name,
          email,
          password,
          role,
        });

        if (response?.data?.access_token) {
          setAccessToken(response.data.access_token);
        }
      } else {
        const response = await authApi.login({
          email,
          password,
        });

        const token =
          response?.data?.access_token ||
          response?.data?.token ||
          response?.data?.accessToken;

        if (token) {
          setAccessToken(token);
        }
      }

      navigate("/dashboard");
    } catch (err) {
      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Something went wrong. Please check your details and try again.";

      setError(
        typeof message === "string"
          ? message
          : "Unable to complete authentication.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background lg:grid lg:grid-cols-[1.15fr_.85fr]">
      {/* LEFT */}
      <section className="relative px-5 py-6 sm:px-8 sm:py-8 lg:px-12 lg:py-10 xl:px-16">
        <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_10%_10%,var(--glow-a),transparent_32%),radial-gradient(circle_at_90%_20%,var(--glow-b),transparent_26%)]" />

        <div className="mx-auto max-w-5xl">
          {/* Branding */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.26em] text-accent">
                {LOGIN_CONFIG.eyebrow}
              </p>

              <p className="mt-1 font-display text-xl font-bold tracking-tight text-primary">
                {LOGIN_CONFIG.brand}
              </p>
            </div>

            <div className="hidden rounded-full border border-border/80 bg-card/70 px-3 py-1.5 text-xs text-muted-foreground backdrop-blur sm:block">
              Built for rapid iteration
            </div>
          </div>

          {/* Hero */}
          <div className="relative overflow-hidden rounded-[2rem] border border-border/70 bg-black shadow-[var(--shadow-lift)]">
            <div className="relative h-[360px] sm:h-[500px] lg:h-[540px]">
              {SLIDES.map((image, index) => (
                <img
                  key={image.src}
                  src={image.src}
                  alt={image.alt}
                  loading={index === 0 ? "eager" : "lazy"}
                  className={`absolute inset-0 h-full w-full object-cover transition-all duration-[1200ms] ease-out ${
                    index === slide
                      ? "scale-100 opacity-100"
                      : "scale-105 opacity-0"
                  }`}
                />
              ))}

              <div className="absolute inset-0 bg-gradient-to-t from-primary/95 via-primary/45 to-transparent" />
              <div className="absolute inset-0 bg-gradient-to-br from-accent/20 via-transparent to-transparent" />

              <div className="absolute inset-x-0 bottom-0 p-6 sm:p-10 lg:p-12">
                <p className="mb-3 text-xs font-semibold uppercase tracking-[0.28em] text-accent-foreground/90">
                  {LOGIN_CONFIG.story.kicker}
                </p>

                <div className="relative h-14 sm:h-20">
                  {LOGIN_CONFIG.story.taglines.map((text, index) => (
                    <h1
                      key={text}
                      className={`font-display absolute inset-0 text-4xl font-black leading-tight text-primary-foreground transition-opacity duration-700 sm:text-6xl ${
                        index === tagline ? "opacity-100" : "opacity-0"
                      }`}
                    >
                      {text}
                    </h1>
                  ))}
                </div>

                <p className="mt-4 max-w-xl text-sm leading-relaxed text-primary-foreground/80 sm:text-base">
                  {LOGIN_CONFIG.subheading}
                </p>
              </div>

              <button
                type="button"
                onClick={prev}
                aria-label="Previous image"
                className="absolute left-4 top-1/2 -translate-y-1/2 rounded-full border border-white/15 bg-black/20 p-2 text-white backdrop-blur-md transition hover:bg-black/35"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>

              <button
                type="button"
                onClick={next}
                aria-label="Next image"
                className="absolute right-4 top-1/2 -translate-y-1/2 rounded-full border border-white/15 bg-black/20 p-2 text-white backdrop-blur-md transition hover:bg-black/35"
              >
                <ChevronRight className="h-5 w-5" />
              </button>

              <div className="absolute right-6 top-6 flex gap-2">
                {SLIDES.map((image, index) => (
                  <button
                    type="button"
                    key={image.src}
                    onClick={() => setSlide(index)}
                    aria-label={`Go to slide ${index + 1}`}
                    className={`h-2 rounded-full transition-all ${
                      index === slide
                        ? "w-7 bg-accent"
                        : "w-2 bg-white/50 hover:bg-white/80"
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Story card */}
          <div className="mt-6 rounded-[1.7rem] border border-border/80 bg-card/80 p-5 shadow-[var(--shadow-soft)] backdrop-blur sm:p-6">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="inline-flex rounded-full bg-secondary p-1">
                {["purpose", "impact"].map((item) => (
                  <button
                    type="button"
                    key={item}
                    onClick={() => setFace(item)}
                    className={`rounded-full px-5 py-2 text-sm font-semibold capitalize transition-all ${
                      face === item
                        ? "bg-primary text-primary-foreground shadow-[var(--shadow-soft)]"
                        : "text-secondary-foreground hover:text-primary"
                    }`}
                  >
                    {item}
                  </button>
                ))}
              </div>

              <Link
                to="/"
                className="hidden text-sm font-semibold text-primary hover:underline sm:inline-flex sm:items-center sm:gap-1"
              >
                Explore app
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>

            <div className="mt-4 [perspective:1400px]">
              <div
                className="flip-card relative h-[132px]"
                style={{
                  transform:
                    face === "impact"
                      ? "rotateY(180deg)"
                      : "rotateY(0deg)",
                }}
              >
                <article className="flip-face absolute inset-0 rounded-2xl border border-border bg-muted/35 p-5">
                  <h2 className="font-display text-lg font-bold text-primary">
                    {LOGIN_CONFIG.story.purposeTitle}
                  </h2>

                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                    {LOGIN_CONFIG.story.purpose}
                  </p>
                </article>

                <article
                  className="flip-face absolute inset-0 rounded-2xl border border-border bg-muted/35 p-5"
                  style={{ transform: "rotateY(180deg)" }}
                >
                  <h2 className="font-display text-lg font-bold text-primary">
                    {LOGIN_CONFIG.story.impactTitle}
                  </h2>

                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                    {LOGIN_CONFIG.story.impact}
                  </p>
                </article>
              </div>
            </div>

            <div className="mt-5 grid grid-cols-1 gap-2 sm:grid-cols-3">
              {LOGIN_CONFIG.story.stats.map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-2xl border border-border bg-background/70 px-4 py-3"
                >
                  <div className="font-display text-lg font-black text-primary">
                    {stat.value}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* RIGHT */}
      <section className="relative flex items-center border-t border-border/60 bg-surface px-5 py-10 sm:px-8 lg:border-l lg:border-t-0 lg:px-10 xl:px-14">
        <div className="absolute inset-y-0 left-0 hidden w-px bg-gradient-to-b from-transparent via-border to-transparent lg:block" />

        <div className="mx-auto w-full max-w-md">
          {/* Heading */}
          <div className="mb-8">
            <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent-soft px-3 py-1.5 text-xs font-semibold text-accent-foreground">
              <Sparkles className="h-3.5 w-3.5" />
              Smart access
            </div>

            <h2 className="font-display text-3xl font-black tracking-tight text-primary sm:text-4xl">
              {mode === "login" ? "Welcome back." : "Create your account."}
            </h2>

            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              {mode === "login"
                ? "Sign in to continue to your workspace."
                : "Create an account and start contributing."}
            </p>
          </div>

          {/* Login/Register */}
          <div className="rounded-[1.75rem] border border-border bg-card p-5 shadow-[var(--shadow-lift)] sm:p-7">
            {/* Mode switch */}
            <div className="mb-6 grid grid-cols-2 rounded-xl bg-secondary p-1">
              {["login", "register"].map((item) => (
                <button
                  type="button"
                  key={item}
                  onClick={() => {
                    setMode(item);
                    setError("");
                  }}
                  className={`rounded-lg px-4 py-2.5 text-sm font-semibold capitalize transition ${
                    mode === item
                      ? "bg-background text-primary shadow-sm"
                      : "text-muted-foreground hover:text-primary"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>

            {/* Role */}
            <div className="mb-6">
              <div className="mb-2 flex items-center justify-between">
                <label className="text-sm font-semibold text-primary">
                  Continue as
                </label>

                <ShieldCheck className="h-4 w-4 text-accent" />
              </div>

              <div className="grid grid-cols-2 gap-2">
                {LOGIN_CONFIG.roles.map((item) => (
                  <button
                    type="button"
                    key={item.id}
                    onClick={() => setRole(item.id)}
                    className={`rounded-xl border p-3 text-left transition ${
                      role === item.id
                        ? "border-primary bg-primary/5 ring-2 ring-primary/10"
                        : "border-border bg-background hover:border-primary/30"
                    }`}
                  >
                    <div className="text-sm font-semibold text-primary">
                      {item.label}
                    </div>
                    <div className="mt-1 text-[11px] leading-4 text-muted-foreground">
                      {item.description}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === "register" && (
                <div>
                  <label className="mb-2 block text-sm font-medium text-primary">
                    Full name
                  </label>

                  <div className="relative">
                    <input
                      value={name}
                      onChange={(event) => setName(event.target.value)}
                      placeholder="Enter your name"
                      className="h-11 w-full rounded-xl border border-border bg-background pl-10 pr-3 text-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/15"
                    />
                    <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                      <CheckCircle2 className="h-4 w-4" />
                    </span>
                  </div>
                </div>
              )}

              <div>
                <label className="mb-2 block text-sm font-medium text-primary">
                  Email
                </label>

                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="you@example.com"
                    className="h-11 w-full rounded-xl border border-border bg-background pl-10 pr-3 text-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/15"
                  />

                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                    <Mail className="h-4 w-4" />
                  </span>
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-primary">
                  Password
                </label>

                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Enter your password"
                    className="h-11 w-full rounded-xl border border-border bg-background pl-10 pr-11 text-sm outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/15"
                  />

                  <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                    <LockKeyhole className="h-4 w-4" />
                  </span>

                  <button
                    type="button"
                    onClick={() => setShowPassword((value) => !value)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground transition hover:text-primary"
                    aria-label={
                      showPassword
                        ? "Hide password"
                        : "Show password"
                    }
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>

              {mode === "login" && (
                <div className="flex justify-end">
                  <button
                    type="button"
                    className="text-xs font-semibold text-accent hover:underline"
                  >
                    Forgot password?
                  </button>
                </div>
              )}

              {error && (
                <div className="rounded-xl border border-destructive/20 bg-destructive/5 px-3 py-2.5 text-sm text-destructive">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 text-sm font-semibold text-primary-foreground shadow-sm transition hover:bg-primary-hover disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading
                  ? "Please wait..."
                  : mode === "login"
                    ? role === "admin"
                      ? "Sign in as admin"
                      : "Continue"
                    : "Create account"}

                {!loading && <ArrowRight className="h-4 w-4" />}
              </button>
            </form>

            {/* Google UI */}
            <div className="my-5 flex items-center gap-3">
              <div className="h-px flex-1 bg-border" />
              <span className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
                or
              </span>
              <div className="h-px flex-1 bg-border" />
            </div>

            <button
              type="button"
              className="flex h-11 w-full items-center justify-center gap-3 rounded-xl border border-border bg-background text-sm font-semibold text-primary transition hover:bg-muted"
            >
              <span className="grid h-5 w-5 place-items-center rounded-full bg-white text-xs font-black">
                G
              </span>
              Continue with Google
            </button>

            <p className="mt-5 text-center text-xs leading-relaxed text-muted-foreground">
              By continuing, you agree to the terms and privacy policy of{" "}
              <span className="font-semibold text-primary">
                {LOGIN_CONFIG.brand}
              </span>
              .
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}