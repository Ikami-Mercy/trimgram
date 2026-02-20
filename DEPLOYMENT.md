# Trimgram Deployment Guide

This guide walks you through deploying Trimgram to production using Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Railway account (free tier available)
- Vercel account (free tier available)
- Code pushed to a GitHub repository

## Backend Deployment (Railway)

### 1. Prepare Your Repository

Ensure your backend code is in the `backend/` directory with:
- `main.py` - FastAPI application entry point
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment variables

### 2. Deploy to Railway

1. Go to [railway.app](https://railway.app/) and sign in with GitHub

2. Click **"New Project"** → **"Deploy from GitHub repo"**

3. Select your Trimgram repository

4. Railway will auto-detect Python and install dependencies from `requirements.txt`

5. Configure the start command:
   - Go to **Settings** → **Deploy**
   - Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Set **Root Directory**: `backend`

6. Set environment variables:
   - Go to **Variables**
   - Add the following:

```
DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.vercel.app
SESSION_TTL_SECONDS=1800
INSTAGRAM_REQUEST_DELAY=2.0
MAX_NON_FOLLOWERS_SHOWN=100
POSTS_TO_ANALYZE=12
UNFOLLOW_DELAY_SECONDS=15.0
PORT=8000
HOST=0.0.0.0
```

7. Deploy:
   - Railway will automatically deploy
   - Note your backend URL (e.g., `https://trimgram-backend.railway.app`)

### 3. Verify Backend Deployment

Visit `https://your-backend-url.railway.app/health`

You should see:
```json
{
  "status": "healthy",
  "active_sessions": 0
}
```

## Frontend Deployment (Vercel)

### 1. Prepare Your Repository

Ensure your frontend code is in the `frontend/` directory with:
- `package.json`
- `vite.config.js`
- `.env.example`

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com/) and sign in with GitHub

2. Click **"Add New Project"** → **"Import Git Repository"**

3. Select your Trimgram repository

4. Configure project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. Set environment variables:
   - Click **"Environment Variables"**
   - Add:

```
VITE_API_URL=https://your-backend-url.railway.app
```

6. Click **"Deploy"**

7. Vercel will build and deploy your frontend
   - Note your frontend URL (e.g., `https://trimgram.vercel.app`)

### 3. Update Backend CORS

Go back to Railway and update the `CORS_ORIGINS` variable:

```
CORS_ORIGINS=https://trimgram.vercel.app
```

This ensures your frontend can communicate with the backend.

### 4. Verify Frontend Deployment

Visit your Vercel URL and test the login flow.

## Post-Deployment Checklist

- [ ] Backend health check endpoint responds correctly
- [ ] Frontend loads without errors
- [ ] Login flow works end-to-end
- [ ] Analysis completes successfully
- [ ] Unfollow functionality works
- [ ] Privacy policy page is accessible
- [ ] GitHub link points to correct repository
- [ ] CORS is configured correctly
- [ ] Environment variables are set properly
- [ ] No secrets are committed to GitHub

## Monitoring & Logs

### Railway (Backend)
- Go to **Deployments** tab to see logs
- Click on a deployment to see real-time logs
- Use `Cmd/Ctrl + K` to search logs

### Vercel (Frontend)
- Go to **Deployments** tab
- Click on a deployment to see build and runtime logs
- Function logs available in **Functions** tab

## Troubleshooting

### Backend Issues

**Problem**: 500 Internal Server Error

**Solution**:
- Check Railway logs for Python errors
- Verify all environment variables are set
- Ensure `requirements.txt` includes all dependencies
- Check that `instagrapi` is installed correctly

**Problem**: CORS errors in browser console

**Solution**:
- Verify `CORS_ORIGINS` in Railway includes your Vercel domain
- Ensure no trailing slashes in CORS origins
- Check that HTTPS is used (not HTTP) in production

### Frontend Issues

**Problem**: "Network Error" or "Failed to fetch"

**Solution**:
- Verify `VITE_API_URL` points to correct Railway URL
- Check that Railway backend is running (visit `/health` endpoint)
- Ensure CORS is configured on backend

**Problem**: Build fails on Vercel

**Solution**:
- Check build logs in Vercel dashboard
- Verify `package.json` is valid
- Ensure all dependencies are listed
- Try building locally first: `npm run build`

## Custom Domain Setup

### For Vercel (Frontend)

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Follow Vercel's DNS configuration instructions
4. Update Railway's `CORS_ORIGINS` to include your custom domain

### For Railway (Backend)

1. Go to **Settings** → **Domains**
2. Click **"Generate Domain"** for a Railway subdomain
3. Or add a custom domain and configure DNS

## Scaling & Performance

### Backend (Railway)

- Railway automatically scales based on traffic
- Monitor memory usage in Railway dashboard
- For high traffic, consider upgrading to Railway Pro plan

### Frontend (Vercel)

- Vercel's CDN automatically handles global distribution
- Static assets are cached at the edge
- No configuration needed for basic scaling

## Security Recommendations

1. **Never commit `.env` files** - use `.env.example` instead
2. **Use HTTPS everywhere** - both Railway and Vercel provide this by default
3. **Rotate secrets regularly** - if credentials are compromised
4. **Monitor logs** - watch for suspicious activity
5. **Rate limiting** - already built into the app
6. **Keep dependencies updated** - run `pip list --outdated` and `npm outdated`

## Cost Estimate

### Free Tier Limits

**Railway Free Tier**:
- $5 free credit per month
- Sufficient for 100-500 users per month
- Sleeps after inactivity (wakes on request)

**Vercel Free Tier**:
- Unlimited bandwidth
- 100 GB-hours compute per month
- Perfect for most use cases

### When to Upgrade

Consider upgrading if:
- Backend memory usage consistently exceeds 512MB
- You have more than 1,000 active users per day
- Backend needs to stay awake 24/7 (Railway Hobby plan)

## Backup & Disaster Recovery

Since Trimgram uses **no database** and **no persistent storage**:
- No backups needed
- All data is session-based
- Redeployment is instant
- No data loss risk

## Updates & Maintenance

### Deploying Updates

**Backend**:
1. Push changes to GitHub
2. Railway auto-deploys from `main` branch
3. Monitor deployment logs

**Frontend**:
1. Push changes to GitHub
2. Vercel auto-deploys from `main` branch
3. Preview deployments available for all PRs

### Dependency Updates

**Backend**:
```bash
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt
```

**Frontend**:
```bash
npm outdated
npm update
```

## Support

For deployment issues:
- Railway: [railway.app/help](https://railway.app/help)
- Vercel: [vercel.com/support](https://vercel.com/support)
- Trimgram: Open an issue on GitHub

---

**Deployment Checklist Complete** ✅

You now have a fully deployed, production-ready Trimgram instance!
