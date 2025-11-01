# Deploy to Vercel - Quick Guide

Deploy your Miami Med Spa Voice AI API to Vercel in under 5 minutes!

## Why Vercel?

✅ **Free tier** - Perfect for small to medium spas
✅ **Auto-deploy** from GitHub - Push code, it deploys automatically
✅ **Fast** - Global CDN, lightning-fast responses
✅ **SSL included** - Automatic HTTPS
✅ **Zero config** - Just connect and deploy

## 🚀 5-Minute Deployment

### Step 1: Sign Up for Vercel (1 minute)

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub

### Step 2: Import Your Project (2 minutes)

1. Click "Add New..." → "Project"
2. Find `med-spa-portal-1` in your repositories
3. Click "Import"
4. Vercel will auto-detect the Python project
5. Click "Deploy"

**That's it!** Vercel will build and deploy your API.

### Step 3: Get Your API URL (30 seconds)

After deployment completes:

1. You'll see: "🎉 Congratulations!"
2. Copy your URL (looks like: `https://med-spa-portal-1.vercel.app`)
3. Test it by visiting: `https://your-url.vercel.app/`

You should see:
```json
{
  "status": "online",
  "service": "Miami Med Spa Voice AI API",
  "version": "1.0.0"
}
```

### Step 4: Test Your Endpoints (1 minute)

Visit these URLs in your browser:

✅ **Health check:**
`https://your-url.vercel.app/`

✅ **Services list:**
`https://your-url.vercel.app/services`

✅ **API documentation:**
`https://your-url.vercel.app/docs`

If all three work - **you're live!** 🎉

## 🔗 Use Your API URL with Voice AI

Now that your API is deployed:

1. Copy your Vercel URL (e.g., `https://med-spa-portal-1.vercel.app`)
2. Open `vapi_assistant_config.json`
3. Replace all instances of `YOUR-API-URL.com` with your Vercel URL
4. Upload to Vapi.ai

Example:
```json
"url": "https://med-spa-portal-1.vercel.app/services"
```

## 📊 Vercel Free Tier Limits

Perfect for most spas:

| Resource | Free Tier | Typical Spa Usage |
|----------|-----------|-------------------|
| Bandwidth | 100 GB/month | ~10,000 bookings |
| Function Executions | 100GB-hours | ~50,000 API calls |
| Build Time | 6,000 minutes | Unlimited for your use |

**Translation:** Free tier handles ~300-500 phone bookings per month easily!

## 🔄 Auto-Deploy from GitHub

Every time you push to GitHub, Vercel auto-deploys:

```bash
# Make changes to your code
git add .
git commit -m "Updated services"
git push

# Vercel automatically deploys the update!
# You'll get an email when it's live
```

## 🌍 Custom Domain (Optional)

Want to use your own domain like `api.miamispa.com`?

1. Go to Vercel Dashboard → Your Project
2. Click "Settings" → "Domains"
3. Add your domain
4. Update DNS records (Vercel shows you how)
5. Done! SSL automatically included

## 🔧 Environment Variables (If Needed)

If you add features that need API keys:

1. Go to Vercel Dashboard → Your Project
2. Click "Settings" → "Environment Variables"
3. Add variables like:
   - `TWILIO_API_KEY` (for SMS notifications)
   - `SENDGRID_API_KEY` (for email confirmations)
   - `SECRET_KEY` (for security)

## 📱 Monitor Your Deployment

Vercel Dashboard shows:
- Real-time deployment status
- API usage statistics
- Error logs
- Performance metrics

Access at: [vercel.com/dashboard](https://vercel.com/dashboard)

## 🐛 Troubleshooting

### Build Failed?

**Check:** Make sure all files are committed to GitHub
```bash
git status
git add .
git commit -m "All files"
git push
```

### API Returns 404?

**Fix:** Make sure `vercel.json` is in your repository root

### "Module not found" error?

**Fix:** Make sure `requirements.txt` includes all dependencies:
```
fastmcp>=0.2.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
```

### Data Not Persisting?

**Note:** Vercel is serverless, so file-based storage (JSON files) resets between deployments.

**Solutions:**

**Option A:** Use Vercel's free PostgreSQL (Recommended for production)
1. Go to Storage tab in Vercel
2. Create Postgres Database (free tier: 256MB)
3. Update code to use database

**Option B:** Keep JSON files (fine for testing/demo)
- Data resets on each deploy
- Perfect for development/testing
- No changes needed

**Option C:** Use external storage
- MongoDB Atlas (free tier)
- Supabase (free tier)
- Firebase (free tier)

For most spas starting out, **Option A** is best for production.

## 🔐 Security Best Practices

### 1. Enable CORS Properly

Already configured in `api_server.py`:
```python
allow_origins=["*"]  # For development
```

For production, update to:
```python
allow_origins=["https://vapi.ai", "https://your-website.com"]
```

### 2. Add Rate Limiting

Install slowapi:
```bash
pip install slowapi
```

Add to `api_server.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/book")
@limiter.limit("10/minute")  # Max 10 bookings per minute
def book_appointment(booking: BookingRequest):
    ...
```

### 3. Monitor Usage

Set up alerts in Vercel for:
- High bandwidth usage
- Error rates
- Response times

## 🚀 Next Steps

1. ✅ Deploy to Vercel (done!)
2. ✅ Test all endpoints
3. ✅ Copy your Vercel URL
4. ✅ Update `vapi_assistant_config.json` with your URL
5. ✅ Upload to Vapi.ai
6. ✅ Buy phone number
7. ✅ Test booking by calling yourself!

## 💡 Pro Tips

### Tip 1: Use Preview Deployments

Every branch gets its own URL:
- `main` branch → Production URL
- `dev` branch → Preview URL for testing

Test changes before going live!

### Tip 2: View Logs in Real-Time

```bash
# Install Vercel CLI
npm i -g vercel

# View logs
vercel logs
```

### Tip 3: Instant Rollback

Made a mistake? Rollback in one click:
1. Go to Deployments tab
2. Find previous working version
3. Click "..." → "Promote to Production"

### Tip 4: Check API Performance

Vercel shows:
- Average response time
- 95th percentile latency
- Error rates
- Most called endpoints

Use this data to optimize!

## 📞 Complete Voice AI Setup Checklist

- [x] Code pushed to GitHub
- [x] Deployed to Vercel
- [x] API URL working (`/`, `/services`, `/docs`)
- [ ] Updated `vapi_assistant_config.json` with Vercel URL
- [ ] Signed up for Vapi.ai
- [ ] Created voice assistant
- [ ] Bought Miami phone number (305/786)
- [ ] Tested by calling yourself
- [ ] Updated website with phone number
- [ ] Trained staff on system

## 🎉 You're Live!

Your API is now deployed on Vercel's global CDN. Clients can call your AI receptionist 24/7, and bookings will flow in automatically!

**Your API URL:**
`https://your-project.vercel.app`

**API Docs:**
`https://your-project.vercel.app/docs`

## ❓ Need Help?

- **Vercel Docs:** [vercel.com/docs](https://vercel.com/docs)
- **Vercel Support:** [vercel.com/support](https://vercel.com/support)
- **Your Project Dashboard:** [vercel.com/dashboard](https://vercel.com/dashboard)

---

**Total Time:** ~5 minutes
**Cost:** $0 (free tier)
**Maintenance:** Zero - auto-updates from GitHub

Enjoy your automated booking system! 🚀
