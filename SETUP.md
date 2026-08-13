# BlueTeamers AI Assistant — Safe Setup Guide (other machines)

Run this on **any** machine to get the full platform (Django 8000 + AI service 8001 + React 5173) working. Your own `DEEPSEEK_API_KEY` stays secret — it only ever lives in a local, gitignored `.env` file and is never committed or pushed.

## 1. Prerequisites

- Git
- Node.js **v20+** and npm **v11+** (npm 11 blocks esbuild's postinstall by default — see step 5)
- Python **3.13** (Django 6 requires 3.10+; 3.13 is what the venvs are built with)
- ~2 GB free disk for node_modules + two Python venvs

Check versions:

```sh
node --version && npm --version && python3 --version && git --version
```

## 2. Clone the repo

```sh
git clone https://github.com/Harikagolusu/BlueTeamers-AI-Assistant.git
cd BlueTeamers-AI-Assistant
```

## 3. Create your own AI-service credentials (IMPORTANT)

The only secret needed is for the LLM. Copy the template and put **your own** key in it:

```sh
cd ai_service
cp .env.example .env
```

Edit `ai_service/.env` and set the LLM section to use DeepSeek with **your** key:

```ini
DEVELOPMENT_MODE=true
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-REPLACE_WITH_YOUR_OWN_KEY
DEEPSEEK_MODEL=deepseek-v4-flash
```

- Get a key from https://platform.deepseek.com → API keys → create one.
- `.env` is gitignored (`ai_service/.gitignore` and root `.gitignore`), so **never commit or push this file**. Anyone who clones the repo gets only `.env.example` with placeholder values.
- If you want a different provider, the supported values for `LLM_PROVIDER` are `deepseek | omniroute | ollama | bedrock`. Only `deepseek` needs the key above; `omniroute` uses `OMNIROUTE_API_KEY`, `ollama` needs a local runtime, `bedrock` needs `BEDROCK_REGION` + AWS credentials.

## 4. Frontend env (optional)

`infosecdairies/.env` only sets `VITE_API_BASE_URL` (leave blank to use the Vite dev proxy). Nothing to do unless you change API URLs.

## 5. Install dependencies

```sh
# --- Django backend ---
cd infosecdairies/infosec-backend/backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r ../requirements.txt
python generate_jwt_keys.py      # creates jwt_private.pem + jwt_public.pem
bash setup_dev.sh                # migrate + seed courses
mkdir -p backend/staticfiles
deactivate

# --- AI service ---
cd ../../../ai_service
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
deactivate

# --- React frontend ---
cd ../infosecdairies
npm install
npm approve-scripts esbuild      # required on npm 11 — unblocks esbuild's postinstall
```

> If `npm approve-scripts` isn't available, run `npm install --ignore-scripts` then `npx esbuild --version` to force the binary download.

## 6. Start everything

```sh
cd ../..   # repo root
bash start_all.sh
```

This launches three background services and writes logs to `<repo>/logs/`:
- Django backend → http://localhost:8000
- FastAPI AI service → http://localhost:8001 (docs: `/docs`)
- React frontend → http://localhost:5173

## 7. Verify

```sh
curl -s -o /dev/null -w "frontend %{http_code}\n" http://localhost:5173/
curl -s -o /dev/null -w "django   %{http_code}\n" http://localhost:8000/
curl -s -o /dev/null -w "ai       %{http_code}\n" http://localhost:8001/health
```

All three should return `200`. Then open **http://localhost:5173**, register/login, and chat.

## 8. Troubleshooting

- **Port already in use** → kill stale processes first: `pkill -f "vite --port 5173" ; pkill -f uvicorn ; pkill -f runserver`
- **AI service crashes** → check `logs/ai_service_8001.log`; most common cause is a missing/incorrect `DEEPSEEK_API_KEY`.
- **"White screen" on frontend** → ensure `src/data/` files are present (they are committed now). If you pulled before commit `9859149`, `git pull` again.
- **Frontend network errors** → confirm Django is up on 8000; `/api/*` requests proxy through Vite to localhost:8000.
- **Node 24 + npm 11** → if `npm install` skips esbuild, run `npm approve-scripts esbuild`.

## 9. Security checklist

- [ ] `DEEPSEEK_API_KEY` only in `ai_service/.env` — never committed.
- [ ] Confirm your key is not in git: `git log --all -p | grep -c "sk-"` should be `0`.
- [ ] JWT keys (`jwt_*.pem`) and `db.sqlite3` are gitignored — generated locally, never pushed.
- [ ] Use the placeholder `.env.example` as the only committed config template.