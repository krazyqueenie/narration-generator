#!/usr/bin/env python3
"""
narrate_web.py — A local webpage version of the free narration tool.

Run this file, then open the webpage it gives you in your browser.
Type or paste your script, click Generate, and download the mp3.
No account, no API key, no subscription, no time limit.

SETUP (one-time, in Terminal / Command Prompt):
    pip install flask edge-tts

RUN:
    python narrate_web.py

Then open the link it prints (usually http://127.0.0.1:5050) in your browser.
Leave the terminal window open while you use it — closing it shuts down the page.
"""

import asyncio
import os
import tempfile
import webbrowser
import threading

from flask import Flask, request, send_file, Response

import edge_tts
from edge_tts import communicate as edge_communicate
from edge_tts.constants import TRUSTED_CLIENT_TOKEN
from aiohttp import ClientResponseError

# Experimental endpoint reported working by the edge-tts community.
# This modifies the imported constant inside communicate.py, not the package on disk.
edge_communicate.WSS_URL = (
    "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
    f"?Ocp-Apim-Subscription-Key={TRUSTED_CLIENT_TOKEN}"
)

app = Flask(__name__)


@app.after_request
def disable_browser_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

VOICE_LABELS = {
    "en-US-GuyNeural": "Guy — US male, warm/casual",
    "en-US-AriaNeural": "Aria — US female, clear/professional",
    "en-US-EricNeural": "Eric — US male, calm/steady",
    "en-US-JennyNeural": "Jenny — US female, friendly",
    "en-US-ChristopherNeural": "Christopher — US male, confident",
    "en-US-MichelleNeural": "Michelle — US female, natural",
    "en-US-SteffanNeural": "Steffan — US male, formal",
    "en-US-AnaNeural": "Ana — US female, young/upbeat",
    "en-GB-RyanNeural": "Ryan — British male",
    "en-GB-SoniaNeural": "Sonia — British female",
    "en-GB-ThomasNeural": "Thomas — British male, formal",
    "en-GB-LibbyNeural": "Libby — British female, young",
}


def get_voices():
    """Load only currently available US and British English Edge voices."""
    try:
        available = asyncio.run(edge_tts.list_voices())
        voices = []
        for item in available:
            locale = item.get("Locale", "")
            short_name = item.get("ShortName", "")
            if locale not in {"en-US", "en-GB"} or not short_name:
                continue

            friendly = item.get("FriendlyName", short_name)
            gender = item.get("Gender", "")
            region = "US" if locale == "en-US" else "British"
            fallback = f"{short_name.replace('Neural', '').split('-')[-1]} — {region} {gender.lower()}"
            label = VOICE_LABELS.get(short_name, fallback)
            voices.append((short_name, label))

        # Guy first when available, then US voices, then British voices.
        voices.sort(key=lambda v: (
            0 if v[0] == "en-US-GuyNeural" else 1,
            0 if v[0].startswith("en-US-") else 1,
            v[1].lower(),
        ))
        return voices
    except Exception:
        # Safe fallback if Microsoft's voice catalog cannot be reached.
        return list(VOICE_LABELS.items())


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Narration Generator</title>
<style>
  :root {
    --bg: #14161a;
    --panel: #1d2026;
    --text: #eceef1;
    --muted: #9aa1ab;
    --accent: #5b8cff;
    --accent-hover: #4677f0;
    --border: #2b2f37;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    padding: 40px 20px;
  }
  .card {
    width: 100%;
    max-width: 640px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px;
  }
  h1 {
    font-size: 20px;
    margin: 0 0 4px;
  }
  p.sub {
    color: var(--muted);
    margin: 0 0 24px;
    font-size: 14px;
  }
  label {
    display: block;
    font-size: 13px;
    color: var(--muted);
    margin-bottom: 6px;
    margin-top: 18px;
  }
  textarea {
    width: 100%;
    min-height: 220px;
    background: #10121600;
    background-color: #0f1114;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 14px;
    line-height: 1.5;
    resize: vertical;
  }
  select, input[type=text] {
    width: 100%;
    background-color: #0f1114;
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 14px;
  }
  .row {
    display: flex;
    gap: 14px;
  }
  .row > div { flex: 1; }
  button {
    margin-top: 24px;
    width: 100%;
    background: var(--accent);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
  }
  button:hover { background: var(--accent-hover); }
  button:disabled { background: #3a3f47; cursor: not-allowed; }
  #status {
    margin-top: 14px;
    font-size: 13px;
    color: var(--muted);
    min-height: 18px;
  }
  #result { margin-top: 18px; }
  audio { width: 100%; margin-top: 10px; }
  a.download {
    display: inline-block;
    margin-top: 10px;
    color: var(--accent);
    text-decoration: none;
    font-size: 14px;
  }
  .charcount {
    text-align: right;
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
  }
</style>
</head>
<body>
<div class="card">
  <h1>Narration Generator</h1>
  <p class="sub">Free, local, no subscription. No length limit — paste a full 20-minute script if you need to.</p>

  <label for="text">Your script</label>
  <textarea id="text" placeholder="Paste or type your narration here..."></textarea>
  <div class="charcount" id="charcount">0 characters</div>

  <div class="row">
    <div>
      <label for="voice">Voice</label>
      <select id="voice">
        {voice_options}
      </select>
    </div>
    <div>
      <label for="rate">Speed</label>
      <select id="rate">
        <option value="-20%">Slower</option>
        <option value="+0%" selected>Normal</option>
        <option value="+15%">Faster</option>
      </select>
    </div>
  </div>

  <button id="genBtn" onclick="generate()">Generate Narration</button>
  <div id="status"></div>
  <div id="result"></div>
</div>

<script>
const textEl = document.getElementById('text');
const charcount = document.getElementById('charcount');
textEl.addEventListener('input', () => {
  charcount.textContent = textEl.value.length + ' characters';
});

async function generate() {
  const text = textEl.value.trim();
  const voice = document.getElementById('voice').value;
  const rate = document.getElementById('rate').value;
  const statusEl = document.getElementById('status');
  const resultEl = document.getElementById('result');
  const btn = document.getElementById('genBtn');

  if (!text) {
    statusEl.textContent = 'Type or paste some text first.';
    return;
  }

  btn.disabled = true;
  statusEl.textContent = 'Generating... this can take a bit for long scripts.';
  resultEl.innerHTML = '';

  try {
    const resp = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, voice, rate })
    });

    if (!resp.ok) {
      const errText = await resp.text();
      throw new Error(errText || 'Generation failed');
    }

    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);

    resultEl.innerHTML = `
      <audio controls src="${url}"></audio>
      <br>
      <a class="download" href="${url}" download="narration.mp3">Download narration.mp3</a>
    `;
    statusEl.textContent = 'Done.';
  } catch (err) {
    statusEl.textContent = 'Error: ' + err.message;
  } finally {
    btn.disabled = false;
  }
}
</script>
</body>
</html>
"""


def render_page():
    options_html = "\n".join(
        f'<option value="{code}">{label}</option>' for code, label in get_voices()
    )
    return PAGE.replace("{voice_options}", options_html)


@app.route("/")
def index():
    return Response(render_page(), mimetype="text/html")


@app.route("/generate", methods=["POST"])
def generate_audio():
    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    voice = data.get("voice", "en-US-GuyNeural")
    rate = data.get("rate", "+0%")

    if not text:
        return Response("No text provided", status=400)

    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        async def run():
            # One additional attempt only when the new endpoint reports 429 rate limiting.
            for attempt in range(2):
                try:
                    communicate = edge_tts.Communicate(text, voice, rate=rate)
                    await communicate.save(path)
                    return
                except ClientResponseError as exc:
                    if exc.status != 429 or attempt == 1:
                        raise
                    await asyncio.sleep(3)

        asyncio.run(run())
        return send_file(path, mimetype="audio/mpeg", as_attachment=False,
                          download_name="narration.mp3")
    except Exception as e:
        return Response(f"Generation failed: {e}", status=500)
    finally:
        # Clean up after response is sent (best-effort; Flask keeps file open during send)
        threading.Timer(30, lambda: os.path.exists(path) and os.remove(path)).start()


@app.route("/shutdown", methods=["POST"])
def shutdown():
    # Local-only helper used by the launcher so an old copy cannot keep serving stale code.
    threading.Timer(0.25, lambda: os._exit(0)).start()
    return Response("Shutting down", status=200)


def open_browser():
    webbrowser.open("http://127.0.0.1:5050/?fresh=1")


if __name__ == "__main__":
    print("Starting Narration Generator...")
    print("Opening http://127.0.0.1:5050 in your browser.")
    print("Keep this window open while you use the tool. Press Ctrl+C to stop.")
    threading.Timer(1.2, open_browser).start()
    app.run(host="127.0.0.1", port=5050, debug=False)
