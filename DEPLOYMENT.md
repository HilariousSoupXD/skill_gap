# 🚀 Free Deployment Guide for Hackathon

This guide will help you deploy your Campus Skill Gap Analyzer project for free using:
- **Backend**: Render (free tier)
- **Frontend**: Vercel (free tier)

## Prerequisites

1. GitHub account
2. Render account (sign up at https://render.com)
3. Vercel account (sign up at https://vercel.com)

## Step 1: Push Your Code to GitHub

1. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. Create a new repository on GitHub and push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy Backend on Render

1. Go to https://dashboard.render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `csshack-backend` (or any name you prefer)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (root of repo)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Select **Free** plan

5. Click **"Create Web Service"**
6. Wait for deployment to complete (usually 2-5 minutes)
7. Once deployed, copy your backend URL (e.g., `https://csshack-backend.onrender.com`)

**Important**: Note down this URL - you'll need it for the frontend!

## Step 3: Deploy Frontend on Vercel

1. Go to https://vercel.com and sign in
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (should auto-detect)
   - **Output Directory**: `dist` (should auto-detect)

5. **Add Environment Variable**:
   - Click **"Environment Variables"**
   - Add a new variable:
     - **Name**: `VITE_API_BASE_URL`
     - **Value**: Your Render backend URL (e.g., `https://csshack-backend.onrender.com`)
   - Make sure it's enabled for **Production**, **Preview**, and **Development**

6. Click **"Deploy"**
7. Wait for deployment to complete (usually 1-2 minutes)
8. Your app will be live at a URL like `https://your-project.vercel.app`

## Step 4: Test Your Deployment

1. Visit your Vercel frontend URL
2. Test the application:
   - Select a role
   - Input skills
   - Submit and view results
3. If you encounter CORS errors, make sure your Render backend URL is correctly set in Vercel environment variables

## Troubleshooting

### Backend Issues

**Problem**: Backend fails to start
- **Solution**: Check Render logs. Make sure `requirements.txt` includes all dependencies
- Verify `Procfile` exists and has correct command

**Problem**: Database not persisting
- **Solution**: Render free tier has ephemeral storage. For hackathon demo, this is usually fine. If you need persistence, consider upgrading or using an external database.

**Problem**: Backend goes to sleep (free tier)
- **Solution**: Render free tier services sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds. This is normal for free tier.

### Frontend Issues

**Problem**: API calls fail with CORS errors
- **Solution**: 
  1. Verify `VITE_API_BASE_URL` is set correctly in Vercel
  2. Check that backend URL doesn't have trailing slash
  3. Redeploy frontend after setting environment variable

**Problem**: Frontend shows "Failed to connect to Flask backend"
- **Solution**: 
  1. Check that backend is deployed and running on Render
  2. Verify `VITE_API_BASE_URL` environment variable is correct
  3. Check browser console for exact error

**Problem**: Build fails on Vercel
- **Solution**: 
  1. Make sure `package.json` has correct build scripts
  2. Check that all dependencies are listed in `package.json`
  3. Review Vercel build logs for specific errors

## Quick Reference

### Backend URL Format
```
https://your-service-name.onrender.com
```

### Frontend URL Format
```
https://your-project.vercel.app
```

### Environment Variable
```
VITE_API_BASE_URL=https://your-backend-url.onrender.com
```

## Alternative: Railway (Backend)

If Render doesn't work, you can use Railway instead:

1. Go to https://railway.app
2. Create new project from GitHub repo
3. Add Python service
4. Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Railway auto-detects `requirements.txt`

## Alternative: Netlify (Frontend)

If Vercel doesn't work, you can use Netlify:

1. Go to https://netlify.com
2. Import from GitHub
3. Set build directory to `frontend`
4. Build command: `cd frontend && npm install && npm run build`
5. Publish directory: `frontend/dist`
6. Add environment variable: `VITE_API_BASE_URL`

## Notes for Hackathon Judges

- **Free Tier Limitations**: 
  - Render backend may take 30 seconds to wake up if inactive
  - Both services are free and suitable for demo purposes
  - No credit card required

- **Demo Tips**:
  - Wake up the backend before demo by visiting the backend URL
  - Have both URLs ready to share
  - Test the full flow before presentation

## Support

If you encounter issues:
1. Check service logs (Render dashboard / Vercel dashboard)
2. Verify all environment variables are set
3. Ensure code is pushed to GitHub
4. Try redeploying services

Good luck with your hackathon! 🎉

