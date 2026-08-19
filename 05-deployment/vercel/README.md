# Vercel Deployment (Frontend)

Deploy your React frontend to Vercel with automatic builds from GitHub.

## Prerequisites

- Vercel account
- GitHub repository
- Vercel CLI (optional): `npm install -g vercel`

## Setup Steps

### 1. Prepare Your Project

Ensure your `package.json` has a build script:

```json
{
  "scripts": {
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

### 2. Deploy via Web UI

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend` (if applicable)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3. Environment Variables

Add in Vercel dashboard:

```
VITE_API_URL=https://your-api-domain.com
```

### 4. Deploy via CLI

```bash
cd frontend
vercel

# Production deployment
vercel --prod
```

## Custom Domain

1. Go to Project Settings > Domains
2. Add your custom domain
3. Configure DNS records as shown

## Automatic Deployments

- **Production**: Push to `main` branch
- **Preview**: Push to any other branch or open PR

## Environment-Specific Builds

Create multiple environments:

```bash
# Preview environment
vercel

# Production environment
vercel --prod
```

## Rollback

```bash
# List deployments
vercel ls

# Rollback to specific deployment
vercel rollback [deployment-url]
```

## Performance

Vercel automatically provides:
- Global CDN
- Edge caching
- Image optimization
- Automatic HTTPS
- HTTP/2 & HTTP/3

## Monitoring

View analytics in Vercel dashboard:
- Page views
- Performance metrics
- Error tracking
