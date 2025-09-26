# Railway Deployment Guide

## 🚀 Deploy to Railway

Follow these steps to deploy your port scanner to Railway:

### Step 1: Push to GitHub

First, make sure your code is pushed to GitHub:

```powershell
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit - Educational Port Scanner"

# Create repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/port-scanner.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Railway

1. **Go to Railway**: Visit [railway.app](https://railway.app)

2. **Sign up/Login**: Use your GitHub account

3. **Create New Project**: Click "New Project"

4. **Deploy from GitHub**: Select "Deploy from GitHub repo"

5. **Select Repository**: Choose your `port-scanner` repository

6. **Configure Environment Variables** (in Railway dashboard):
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = `your-secret-key-here` (generate a random string)

### Step 3: Automatic Deployment

Railway will automatically:
- Detect Python project from `requirements.txt`
- Install dependencies
- Use the start command from `railway.json`
- Deploy your app

### Step 4: Access Your App

Once deployed, Railway will provide a URL like:
`https://your-app-name.railway.app`

## 🔧 Configuration Files Created

- **`railway.json`**: Railway-specific configuration
- **`Procfile`**: Process file for deployment
- **`requirements.txt`**: Updated with gunicorn for production
- **`runtime.txt`**: Python version specification

## 🔒 Security Features

Your deployed app includes:
- ✅ Target whitelist (only safe test servers)
- ✅ Rate limiting (5 requests/minute per IP)
- ✅ Port range limits (max 50 ports)
- ✅ Input validation
- ✅ Educational disclaimers

## 🌍 Environment Variables

Set these in Railway dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Disables debug mode |
| `SECRET_KEY` | `random-string` | Flask security key |
| `PORT` | (auto-set) | Railway auto-assigns |

## 📝 Legal Compliance

Your deployed app includes:
- Clear educational disclaimers
- Warnings about responsible use
- Target restrictions to prevent abuse
- Rate limiting to prevent overload

## 🛠️ Troubleshooting

### Common Issues:

1. **Build fails**: Check `requirements.txt` formatting
2. **App crashes**: Check environment variables are set
3. **502 errors**: Verify gunicorn is in requirements.txt
4. **Slow response**: This is normal for the first request (cold start)

### Logs:

View logs in Railway dashboard:
- Build logs: Show installation process
- Deploy logs: Show startup messages
- Runtime logs: Show app activity

## 🔄 Updates

To update your deployed app:
1. Make changes locally
2. Commit and push to GitHub
3. Railway automatically redeploys

## 💰 Costs

Railway offers:
- **Free tier**: $5/month credit (usually sufficient for small apps)
- **Pay-as-you-go**: Only pay for usage beyond free tier

## 📊 Monitoring

Railway provides:
- Resource usage metrics
- Request logs
- Error tracking
- Uptime monitoring

Your app is now production-ready for educational use! 🎉