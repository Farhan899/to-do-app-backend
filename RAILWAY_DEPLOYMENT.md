# Railway Deployment Guide

This guide explains how to deploy your FastAPI backend to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your project connected to a GitHub repository (recommended)

## Deployment Steps

### 1. Prepare Your Repository

Make sure your backend directory contains:
- `requirements.txt` with all dependencies
- `Procfile` with the deployment command
- `entrypoint.sh` for running database migrations
- `runtime.txt` specifying Python version
- All application code in the `app/` directory

### 2. Connect Your Project to Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Choose the backend directory if prompted
5. Click "Deploy"

### 3. Configure Environment Variables

After connecting your project, go to the "Variables" tab and add:

```
DATABASE_URL=postgresql://username:password@host:port/database_name
BETTER_AUTH_SECRET=your-secret-key-here
FRONTEND_URL=https://your-frontend-url.vercel.app
```

For the database, you can add a PostgreSQL addon directly in Railway:
1. Go to "Plugins" tab
2. Click "PostgreSQL" (or "Database" depending on options)
3. Click "Provision"

Railway will automatically populate the DATABASE_URL variable with the correct connection string.

### 4. Configure Your Service

1. Go to the "Settings" tab for your service
2. Make sure the build command is set to `pip install -r requirements.txt`
3. The start command is handled by your Procfile: `bash entrypoint.sh uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}`

### 5. Deploy

1. Commit and push your changes to GitHub (including Procfile, entrypoint.sh, and runtime.txt)
2. Railway will automatically deploy when you push to your main branch
3. Or manually trigger a deployment from the Railway dashboard

## Important Notes

- The entrypoint.sh script runs database migrations (`alembic upgrade head`) before starting the application
- The app is configured to use the `PORT` environment variable that Railway provides
- Database migrations are handled automatically on each deployment
- The `DATABASE_URL` environment variable is automatically configured when you add a PostgreSQL addon
- We use Python 3.11 runtime to ensure compatibility with all dependencies
- The requirements.txt file has been updated to use compatible package versions

## Troubleshooting

1. If you get "Database connection refused" errors, make sure:
   - You've added a PostgreSQL addon to your Railway project
   - The DATABASE_URL environment variable is correctly set

2. If migrations fail, check the Railway logs for details:
   - Go to the "Logs" tab in your Railway dashboard
   - Look for specific error messages

3. If your app crashes at startup:
   - Verify all required environment variables are set
   - Check that the requirements.txt file includes all dependencies

4. If installation still fails:
   - The runtime.txt file specifies Python 3.11 for better package compatibility
   - We've updated package versions in requirements.txt to be compatible with this Python version