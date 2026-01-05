# ⚡ Quick Deploy Checklist

## Before You Start
- [ ] Code is pushed to GitHub
- [ ] You have Render and Vercel accounts

## Backend (Render) - 5 minutes
1. Go to https://dashboard.render.com
2. New → Web Service → Connect GitHub repo
3. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Plan: **Free**
4. Deploy → Copy URL (e.g., `https://xxx.onrender.com`)

## Frontend (Vercel) - 3 minutes
1. Go to https://vercel.com
2. Add Project → Import GitHub repo
3. Settings:
   - Root Directory: `frontend`
   - Framework: Vite
4. Environment Variables:
   - `VITE_API_BASE_URL` = Your Render URL (no trailing slash!)
5. Deploy

## Test
Visit your Vercel URL and test the app!

## ⚠️ Important Notes
- Render free tier sleeps after 15 min (first request takes ~30s)
- Wake up backend before demo: visit the Render URL
- No credit card needed for free tiers

See `DEPLOYMENT.md` for detailed instructions.

