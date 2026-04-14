# 📝 AI Omluvenkář — Setup Guide

A mini school project: a web app that turns casual student excuses into
formal excuse letters using a local LLM (Ollama), Flask, PostgreSQL, and Docker.

---

## Project Structure

```
ai-excuse-generator/
├── app.py                  # Flask backend (routes + DB logic)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Builds the Flask container
├── docker-compose.yml      # Spins up Flask + Ollama + PostgreSQL
└── templates/
    └── index.html          # Web UI with template dropdown
```

---

## Step-by-Step Setup

### 1. Start all three services
```bash
docker compose up --build
```
This starts:
- **`db`** — PostgreSQL on the internal network
- **`ollama`** — the LLM engine
- **`web`** — the Flask app on port 5005

Flask will automatically create the `templates` table and seed it with
6 starter templates on first boot.

### 2. Pull the AI model (one-time)
```bash
docker exec ollama ollama pull phi3
```

### 3. Optional: custom local domain
```bash
echo "127.0.0.1 tobik.skola.test" | sudo tee -a /etc/hosts
```

### 4. Open the app
```
http://tobik.skola.test:5005
# or
http://localhost:5005
```

---

## How to use
1. Pick a **template** from the dropdown — it pre-fills the text box
2. Edit the excuse to fit your situation
3. Click **Generate Formal Letter**
4. Copy the result ✓

---

## Useful commands

```bash
# Stop everything
docker compose down

# Connect to the database directly (for debugging)
docker exec -it excuse_db psql -U student -d excuses

# View templates in the DB
SELECT * FROM templates;

# Add your own template
INSERT INTO templates (name, text) VALUES ('My reason', 'I had a dentist appointment.');
```

---

## Architecture

```
Browser (index.html)
    │
    ├── GET  /templates  →  Flask reads from PostgreSQL → returns JSON list
    │                       (populates the dropdown on page load)
    │
    └── POST /generate   →  Flask calls Ollama API → returns formal letter

Docker network "excuse_net":
  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐
  │  web:5005   │───▶│  db:5432     │    │  ollama:11434 │
  │  (Flask)    │    │  (PostgreSQL)│    │  (LLM engine) │
  └─────────────┘    └──────────────┘    └───────────────┘
```

All three containers communicate by **service name** over the shared
bridge network — no IP addresses needed.
