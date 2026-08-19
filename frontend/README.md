# Hackathon Frontend Boilerplate

Generic React + Vite + Tailwind starter for 12-hour hackathons.

## Included

- React + Vite
- Tailwind CSS v4
- React Router
- TanStack Query
- Axios API client
- PWA support
- Framer Motion
- Recharts
- Swiper
- Sonner
- React Hook Form + Zod-ready setup
- Lucide icons
- Generic login/authentication starter
- Reusable Card, Badge, Input and Skeleton primitives
- Dashboard, feature, loading, error and empty-state examples

## Run

```bash
npm install
npm run dev
```

Create `.env` from `.env.example` and set the backend API URL.

## Authentication

`/login` contains a reusable visual login/register/admin starter. The form is intentionally UI-only until you connect it to the team's backend API. `src/api/auth.js` contains the generic endpoint contract.

## Philosophy

Keep the core boilerplate small. Add specialized libraries such as maps, AI SDKs, realtime sockets or advanced offline sync only when the problem statement requires them.
