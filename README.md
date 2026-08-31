# Crop Condition Predictor — Vercel deployment

A Flask app with a scikit-learn decision tree, deployed to Vercel as a
Python serverless function.

## Structure
```
crop-predictor-vercel/
├── api/
│   └── index.py       # Flask app: serves the page + /api/predict, /api/data
├── requirements.txt    # Python deps
├── vercel.json          # Routes all requests to the Python function
└── README.md
```

## Deploy

### Option A — Vercel CLI (fastest)
```bash
npm i -g vercel        # if you don't have it
cd crop-predictor-vercel
vercel                 # follow prompts, deploys to a preview URL
vercel --prod           # promote to production
```

### Option B — GitHub + Vercel dashboard
1. Push this folder to a GitHub repo.
2. Go to vercel.com → "Add New Project" → import the repo.
3. Vercel auto-detects `vercel.json` and the Python runtime — no extra
   config needed. Click Deploy.

## Local testing
```bash
pip install -r requirements.txt
python api/index.py
# open http://localhost:5000
```

## Notes
- The model retrains on every cold start (it's a 20-row dataset, so this
  is instantaneous — no need to pickle/save it).
- `/api/predict` (POST, JSON `{temp, hum, rain}`) returns `{"condition": "Good"|"Poor"}`.
- `/api/data` (GET) returns the raw dataset as JSON.
- If you'd rather not touch Python hosting quirks at all, the original
  static `crop-predictor.html` will also deploy to Vercel as-is (zero
  config, since Vercel serves static files natively) — just drop it in a
  folder and deploy. The Flask version above is only needed if you want
  the prediction logic to genuinely run in Python server-side.
