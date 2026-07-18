# Ask Kochi MVP

A small AI travel-planning app for Kochi. It has two deploys only:

- **Vercel** hosts the Vite frontend.
- **Render** hosts the FastAPI API and keeps the Gemini key private.

There is no database, Firebase, Docker, user account, conversation history, or separate data
service. Chat is intentionally stateless. The AI is guarded against inventing live opening hours,
events, prices, bookings, routes, and safety information.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
cp .env.example .env
make frontend-install
```

Add your Gemini key to the one root `.env` file:

```text
ASK_KOCHI_GEMINI_API_KEY=your_key_here
```

Start both services in separate terminals:

```bash
make run
make frontend-run
```

Open `http://127.0.0.1:5173`.

## Deploy

### 1. Render API

Create a Render **Web Service** from this repository:

```text
Root Directory: .
Build Command: pip install .
Start Command: uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT
Health Check Path: /api/v1/health
```

Set these Render environment variables:

```text
ASK_KOCHI_ENVIRONMENT=production
ASK_KOCHI_GEMINI_API_KEY=<your Gemini API key>
ASK_KOCHI_CORS_ORIGINS=https://<your-vercel-project>.vercel.app
```

Deploy and copy the Render API URL, such as `https://ask-kochi-api.onrender.com`.

### 2. Vercel frontend

Import the same repository into Vercel and use:

```text
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Add this Vercel environment variable:

```text
VITE_API_BASE_URL=https://<your-render-service>.onrender.com/api/v1
```

Deploy Vercel. Copy the final Vercel domain into Render’s `ASK_KOCHI_CORS_ORIGINS` value and
redeploy Render once. If you later attach a custom domain, update that CORS value again.

## Checks

```bash
make test
make lint
make frontend-build
```

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Render health check. |
| `POST` | `/api/v1/chat` | Guarded stateless Gemini travel guidance. |
