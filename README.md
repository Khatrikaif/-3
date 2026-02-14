# Local Minimal Chat App

A fully local, minimal interactive chat app using only:
- HTML/CSS/Vanilla JS (frontend)
- Python + FastAPI (backend)

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

## Notes
- In-memory rooms/messages (no external DB)
- Lightweight polling for near-realtime updates
- Designed to use minimal resources
