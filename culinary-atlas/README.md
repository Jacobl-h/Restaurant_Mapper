# The Culinary Atlas

A luxury restaurant mapping app powered by Google Places, with Michelin star cross-referencing. Your API key lives securely on Vercel — it never touches the browser.

---

## Deploy in 5 minutes

### 1. Push to GitHub

Create a new repo on GitHub, then:

```bash
git init
git add .
git commit -m "initial"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Import into Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import your GitHub repo
3. Leave all build settings as defaults (Vercel auto-detects the config)
4. Click **Deploy** — it will fail the first time because the API key isn't set yet. That's fine.

### 3. Add your API key

1. In your Vercel project, go to **Settings → Environment Variables**
2. Add a new variable:
   - **Name:** `GOOGLE_API_KEY`
   - **Value:** your Google Places API key
   - **Environment:** Production, Preview, Development (check all three)
3. Click **Save**

### 4. Redeploy

Go to **Deployments → ⋯ → Redeploy** on your latest deployment. Your app is now live.

---

## Google API key setup

You need a key with these APIs enabled in [Google Cloud Console](https://console.cloud.google.com):

- **Places API** (for restaurant search + details)
- **Geocoding API** (for address → coordinates)

To enable them:
1. Go to **APIs & Services → Library**
2. Search for and enable **Places API** and **Geocoding API**
3. Go to **APIs & Services → Credentials → Create Credentials → API Key**
4. (Optional but recommended) Restrict the key to only those two APIs

Typical cost: well under $1 for normal personal use. Google gives $200/month free credit.

---

## How the key stays secret

```
Browser  →  /api/geocode?address=...   →  Vercel function  →  Google (with key)
Browser  →  /api/places?lat=...        →  Vercel function  →  Google (with key)
Browser  →  /api/details?place_id=...  →  Vercel function  →  Google (with key)
```

The key is stored as a Vercel environment variable. It only ever exists server-side inside the function process. Inspecting network traffic in the browser shows calls to your own domain only.

---

## Project structure

```
culinary-atlas/
├── api/
│   ├── geocode.js     — proxies Google Geocoding API
│   ├── places.js      — proxies Google Places Nearby Search (all pages)
│   └── details.js     — proxies Google Place Details (lazy, per click)
├── public/
│   └── index.html     — the full frontend (self-contained)
├── vercel.json        — routes /api/* to functions, /* to public/
├── package.json
└── README.md
```

---

## Local development

```bash
npm install -g vercel   # one-time
vercel dev              # starts local server at localhost:3000
```

Create a `.env.local` file (git-ignored) for local dev:

```
GOOGLE_API_KEY=your_key_here
```

---

## Michelin data

Michelin star data is loaded at runtime from the open dataset maintained at  
[github.com/ngshiheng/michelin-my-maps](https://github.com/ngshiheng/michelin-my-maps).  
It covers ~3,500 starred restaurants worldwide and is cross-referenced by name proximity matching — no additional API key needed.
