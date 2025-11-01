# Voice AI Phone Assistant Setup Guide

This guide will help you set up a voice AI phone line for your Miami Med Spa where clients can call and book appointments using natural conversation.

## 🎯 What You'll Get

- **Phone number** clients can call (e.g., 305-XXX-XXXX)
- **AI voice assistant** that answers calls 24/7
- **Natural conversation** - clients talk normally, no button pressing
- **Automatic booking** - appointments saved to your system
- **Professional voice** - sounds like a real receptionist

## 📋 Prerequisites

- Your med spa FastMCP server (already built ✓)
- Internet connection
- Credit card for voice AI service (~$50-100/month for typical usage)

## 🚀 Quick Start (5 Steps)

### Step 1: Deploy Your API Server

Your API needs to be accessible from the internet so the voice AI can call it.

**⭐ Option A: Use Vercel (RECOMMENDED - 5 minutes, FREE)**

Vercel is the easiest and fastest option with auto-deploy from GitHub!

👉 **[See detailed Vercel guide](VERCEL_DEPLOYMENT.md)**

Quick steps:
1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Click "Add New..." → "Project"
3. Import your `med-spa-portal-1` repository
4. Click "Deploy"
5. Copy your URL (looks like: `https://med-spa-portal-1.vercel.app`)

**Benefits:**
- ✅ Free tier (enough for most spas)
- ✅ Auto-deploy from GitHub
- ✅ Global CDN (super fast)
- ✅ SSL included
- ✅ Zero configuration needed

**Option B: Use Replit (Good alternative)**

1. Go to [replit.com](https://replit.com)
2. Sign up/login
3. Click "Create Repl" → "Import from GitHub"
4. Paste your repository URL
5. Click "Run" button
6. Copy the URL (looks like: `https://your-repl.repl.co`)

**Option C: Use Railway**

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your med-spa-portal-1 repo
5. Add start command: `uvicorn api_server:app --host 0.0.0.0 --port 8000`
6. Copy the public URL

**Option D: Use Your Own Server**

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python api_server.py
```

Then expose it using ngrok or your hosting provider.

### Step 2: Test Your API

Open your browser and visit:
```
https://YOUR-API-URL.com/
```

You should see:
```json
{
  "status": "online",
  "service": "Miami Med Spa Voice AI API",
  "version": "1.0.0"
}
```

Test the services endpoint:
```
https://YOUR-API-URL.com/services
```

You should see your list of services (Botox, fillers, etc.)

### Step 3: Sign Up for Vapi.ai (Voice AI Platform)

1. Go to [vapi.ai](https://vapi.ai)
2. Click "Sign Up"
3. Choose the Starter plan (~$0.05/minute)
4. Complete registration
5. Go to Dashboard

### Step 4: Create Your Voice Assistant

In Vapi.ai dashboard:

1. Click "Create Assistant"
2. Click "Import from JSON"
3. Open `vapi_assistant_config.json` from your project
4. Replace `YOUR-API-URL.com` with your actual API URL (from Step 1)
   - Do this in 4 places in the JSON file
5. Paste the updated JSON
6. Click "Create"

**Customize the voice (optional):**
- In Voice settings, try different voices
- Recommended: "Rachel" or "Bella" for professional spa vibe
- Adjust speed/stability to your preference

### Step 5: Get a Phone Number

In Vapi.ai dashboard:

1. Go to "Phone Numbers"
2. Click "Buy Number"
3. Search for Miami area code (305 or 786)
4. Select a number you like
5. Click "Purchase" (~$1-2/month)
6. Assign it to your assistant
7. Click "Save"

**🎉 DONE! Your voice AI is live!**

## 📞 Testing Your Voice AI

1. Call your new number from your phone
2. The AI should answer and greet you
3. Say: "I want to book Botox"
4. Follow the conversation
5. After booking, check your data files to confirm it was saved

## 💰 Costs Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| Phone Number | $1-2/month | One-time + monthly |
| Voice AI (Vapi.ai) | $0.05/minute | Only pay for actual call time |
| API Hosting (Replit) | Free - $7/month | Free tier available |
| **Total** | **~$20-50/month** | For ~200-400 minutes of calls |

**Example:** If you get 50 calls/month averaging 3 minutes each:
- 150 minutes × $0.05 = $7.50 in call costs
- Total: ~$10-15/month

Much cheaper than hiring a receptionist!

## 🎨 Customization Options

### Change the Voice

Edit `vapi_assistant_config.json`:

```json
"voice": {
  "provider": "11labs",
  "voiceId": "21m00Tcm4TlvDq8ikWAM",  // Change this to different voice ID
  "stability": 0.5,
  "similarityBoost": 0.75
}
```

Popular voice IDs:
- `21m00Tcm4TlvDq8ikWAM` - Rachel (Calm, professional)
- `EXAVITQu4vr4xnSDxMaL` - Bella (Friendly, warm)
- `pNInz6obpgDQGcFmaJgB` - Adam (Male, professional)

### Change the Greeting

Edit the `firstMessage` in `vapi_assistant_config.json`:

```json
"firstMessage": "Your custom greeting here"
```

### Add Your Spa Address

In the system prompt, replace `[YOUR SPA ADDRESS]` with your actual address.

### Enable Text Reminders

Add to your API server to send SMS confirmations after booking (requires Twilio account).

## 🔧 Advanced Features

### Call Recording

Already enabled in config. Access recordings in Vapi dashboard.

### Analytics

Vapi provides:
- Call duration statistics
- Conversion rates (calls → bookings)
- Peak call times
- Most requested services

### Multi-Language Support

Add Spanish support for Miami:

```json
"model": {
  "systemPrompt": "...You are bilingual in English and Spanish. If caller speaks Spanish, respond in Spanish..."
}
```

### Business Hours

Modify the greeting based on time:

```json
"firstMessage": "Thank you for calling Miami Med Spa. Our office hours are Monday-Saturday 9am-6pm. I can help you book an appointment right now!"
```

## 🐛 Troubleshooting

### "API not responding" error

**Fix:** Make sure your API server is running
```bash
python api_server.py
```

Visit `YOUR-API-URL.com` in browser - should say "online"

### Voice sounds robotic

**Fix:** In `vapi_assistant_config.json`, adjust:
```json
"temperature": 0.9  // Higher = more natural (0.7 to 1.0)
```

### AI doesn't understand client requests

**Fix:** Update the system prompt with more examples of how people ask for services.

### Calls drop or timeout

**Fix:** Increase timeout in config:
```json
"maxDurationSeconds": 900  // 15 minutes
```

### API calls failing during booking

**Fix:** Check your API logs:
```bash
# View last 50 lines of logs
tail -f api_server.log
```

## 📊 Monitoring Your System

### View Bookings

```bash
# See all appointments
cat data/appointments.json | python -m json.tool

# See all clients
cat data/clients.json | python -m json.tool
```

### API Endpoints You Can Monitor

- `GET /services` - List all services
- `GET /availability/2025-11-15` - Check availability for date
- `POST /book` - Create booking
- `GET /appointment/APT0001` - Get appointment details

### Set Up Notifications

Add webhook to your API to get notified of new bookings:

```python
# In api_server.py, after booking succeeds:
send_email_notification(booking_details)
send_sms_notification(booking_details)
```

## 🔐 Security Best Practices

1. **Enable HTTPS** - Always use secure connections
2. **Rate limiting** - Prevent spam calls (built into Vapi)
3. **HIPAA compliance** - Already enabled in config
4. **Data backup** - Backup your `data/` folder regularly

## 📱 Integration with Your Website

Add "Call Us Now" button:

```html
<a href="tel:+1305XXXXXXX" class="call-button">
  📞 Call to Book - AI Available 24/7
</a>
```

## 🎓 Example Conversations

### Example 1: Simple Booking

**Caller:** "Hi, I want Botox"
**AI:** "Great choice! Botox is one of our most popular treatments. Let me check availability. What date works for you?"
**Caller:** "Tomorrow"
**AI:** "Perfect! Tomorrow I have Dr. Rodriguez available at 2pm, 3:30pm, or 4:15pm."
**Caller:** "2pm works"
**AI:** "Wonderful! Can I get your name and phone number?"
**Caller:** "Maria Lopez, 305-555-1234"
**AI:** "Thank you Maria! I have you booked for Botox with Dr. Rodriguez tomorrow at 2pm. The treatment is 30 minutes and $400. We'll see you at [spa address]. Anything else I can help with?"
**Caller:** "No, that's all"
**AI:** "Perfect! We look forward to seeing you tomorrow at 2pm. Have a great day!"

### Example 2: Service Question

**Caller:** "What services do you offer?"
**AI:** "We offer several treatments: Botox and dermal fillers for wrinkle reduction, hydrafacials and chemical peels for skin rejuvenation, laser hair removal, microneedling, and CoolSculpting for body contouring. What interests you most?"

### Example 3: Rescheduling

**Caller:** "I need to cancel my appointment"
**AI:** "I can help with that. What's your phone number?"
**Caller:** "305-555-1234"
**AI:** "I found your appointment for Botox tomorrow at 2pm. Would you like to cancel or reschedule?"
**Caller:** "Reschedule to next week"
**AI:** "Sure! What day next week works best?"

## 📞 Next Steps

1. ✅ Deploy your API (Step 1)
2. ✅ Sign up for Vapi.ai (Step 3)
3. ✅ Create assistant (Step 4)
4. ✅ Get phone number (Step 5)
5. ✅ Test it yourself
6. ✅ Update your website with the new number
7. ✅ Train your staff on the system
8. ✅ Monitor bookings daily

## 💡 Pro Tips

- **Record the first few calls** and listen to improve the prompts
- **A/B test different greetings** to see what converts better
- **Monitor peak call times** to staff accordingly
- **Add special offers** in the greeting: "First-time clients get 10% off!"
- **Integrate with your calendar** for real-time availability

## 🆘 Support

If you need help:
1. Check Vapi.ai documentation: [docs.vapi.ai](https://docs.vapi.ai)
2. Test your API endpoints directly in browser
3. Review call recordings in Vapi dashboard
4. Check the troubleshooting section above

## 🎉 You're Ready!

Your Miami Med Spa now has a professional AI phone assistant that can:
- Answer calls 24/7
- Book appointments automatically
- Answer service questions
- Sound friendly and professional
- Save you time and money

**Your clients can now call and book in under 2 minutes!**

Questions? Test it yourself first, then share the number with friends/family for feedback before going live with customers.
