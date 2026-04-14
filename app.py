from flask import Flask, request, jsonify, render_template
import requests
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# ── App config ────────────────────────────────────────────────────────────
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

# ── PostgreSQL config (values come from docker-compose environment) ──────────
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "excuses")
DB_USER = os.environ.get("DB_USER", "student")
DB_PASS = os.environ.get("DB_PASS", "tajneheslo")

SYSTEM_PROMPT = """You are a formal school secretary who writes polite, professional excuse letters.
When given a casual student excuse, rewrite it into a formal letter addressed to a teacher.
The letter should be respectful, brief (3-4 sentences), and written in third person.
Start with 'Dear Teacher,' and end with 'Yours sincerely, Parent/Guardian.'
Do not add any extra commentary — only output the letter itself."""


def get_db():
    """Open and return a new PostgreSQL connection."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )


def init_db():
    """Create the templates table and seed it with starter data if empty."""
    conn = get_db()
    cur = conn.cursor()

    # Create table if it doesn't exist yet
    cur.execute("""
        CREATE TABLE IF NOT EXISTS templates (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            text TEXT         NOT NULL
        );
    """)

    # Only insert seed data if the table is empty
    cur.execute("SELECT COUNT(*) FROM templates;")
    if cur.fetchone()[0] == 0:
        seeds = [
            ("Illness",      "I was sick and couldn't get out of bed."),
            ("Oversleeping", "I overslept because I forgot to set my alarm."),
            ("Family event", "I had an important family event I had to attend."),
            ("Doctor visit", "I had a doctor's appointment that ran very late."),
            ("Transport",    "My bus was cancelled and there was no other way to get to school."),
            ("Gaming night", "I was gaming all night and couldn't wake up in the morning."),
        ]
        cur.executemany(
            "INSERT INTO templates (name, text) VALUES (%s, %s);",
            seeds,
        )

    conn.commit()
    cur.close()
    conn.close()


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/templates", methods=["GET"])
def get_templates():
    """Return all templates as JSON — used by the frontend dropdown."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, text FROM templates ORDER BY id;")
    templates = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list(templates))


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    casual_excuse = data.get("excuse", "").strip()

    if not casual_excuse:
        return jsonify({"error": "No excuse provided."}), 400

    prompt = f"Student's casual excuse: \"{casual_excuse}\"\n\nPlease write the formal excuse letter:"

    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            },
            headers=headers,
            timeout=120,
        )
        response.raise_for_status()
        
        # OpenAI format returns choices -> message -> content
        resp_json = response.json()
        letter = ""
        if "choices" in resp_json and len(resp_json["choices"]) > 0:
            letter = resp_json["choices"][0].get("message", {}).get("content", "").strip()
            
        return jsonify({"letter": letter})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to the AI API."}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "AI API took too long to respond. Try again."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Startup ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import time
    # Retry loop: PostgreSQL can take a few seconds to be ready
    for attempt in range(10):
        try:
            init_db()
            print("✅ Database ready.")
            break
        except Exception as e:
            print(f"⏳ Waiting for database... ({attempt + 1}/10): {e}")
            time.sleep(3)

    app.run(host="0.0.0.0", port=5005, debug=True)
