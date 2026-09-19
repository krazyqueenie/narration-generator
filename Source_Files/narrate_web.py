#!/usr/bin/env python3
"""
Narration Generator — native pywebview desktop app.

No local Flask server.
No browser window.
No Command Prompt is required for the packaged EXE.
"""

import asyncio
import base64
import json
import os
import tempfile

import edge_tts
import webview


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


def _language_label(item):
    locale = item.get("Locale", "")
    friendly = item.get("FriendlyName", "")

    if " - " in friendly:
        readable = friendly.rsplit(" - ", 1)[-1].strip()
        if readable and readable != friendly:
            return readable

    return locale or "Other"


def get_voice_catalog():
    try:
        available = asyncio.run(edge_tts.list_voices())
        voices = []

        for item in available:
            locale = item.get("Locale", "")
            short_name = item.get("ShortName", "")
            if not locale or not short_name:
                continue

            gender = item.get("Gender", "")
            name = short_name.replace("Neural", "").split("-")[-1]
            fallback = f"{name} — {gender.lower()}" if gender else name
            label = VOICE_LABELS.get(short_name, fallback)

            voices.append({
                "code": short_name,
                "label": label,
                "locale": locale,
                "language": _language_label(item),
            })

        voices.sort(key=lambda v: (
            0 if v["locale"] == "en-US" else 1,
            v["language"].lower(),
            0 if v["code"] == "en-US-GuyNeural" else 1,
            v["label"].lower(),
        ))

        return voices

    except Exception:
        voices = []
        for code, label in VOICE_LABELS.items():
            locale = "en-US" if code.startswith("en-US-") else "en-GB"
            language = "English (United States)" if locale == "en-US" else "English (United Kingdom)"
            voices.append({
                "code": code,
                "label": label,
                "locale": locale,
                "language": language,
            })
        return voices


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Narration Generator</title>
<style>
  :root {
    --bg: #0f1118;
    --surface: #171a24;
    --surface-2: #11141c;
    --surface-3: #1d2130;
    --border: #2c3243;
    --border-soft: #252a38;
    --text: #f3f5fb;
    --muted: #929bad;
    --accent: #6f86ff;
    --accent-2: #9a68f5;
    --success: #8fe0b0;
  }
  * { box-sizing: border-box; }
  html, body { width: 100%; height: 100%; margin: 0; }
  body {
    overflow: hidden;
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
  }
  button, textarea, select { font: inherit; }

  .app-shell {
    height: 100vh;
    min-height: 620px;
    display: grid;
    grid-template-rows: 70px 1fr 34px;
    background: var(--bg);
  }

  .titlebar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 0 28px;
    background: #151822;
    border-bottom: 1px solid var(--border-soft);
    box-shadow: 0 1px 0 rgba(255,255,255,.02) inset;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 13px;
    min-width: 0;
  }
  .app-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: grid;
    place-items: center;
    flex: 0 0 auto;
    background: linear-gradient(145deg, rgba(111,134,255,.22), rgba(154,104,245,.22));
    border: 1px solid rgba(137,128,246,.34);
  }
  .wave { display: flex; align-items: center; gap: 2px; height: 20px; }
  .wave span { width: 3px; border-radius: 4px; background: #a9b6ff; }
  .wave span:nth-child(1), .wave span:nth-child(7) { height: 6px; }
  .wave span:nth-child(2), .wave span:nth-child(6) { height: 11px; }
  .wave span:nth-child(3), .wave span:nth-child(5) { height: 16px; }
  .wave span:nth-child(4) { height: 20px; background: #b07cff; }
  .brand-text h1 { margin: 0; font-size: 18px; font-weight: 650; letter-spacing: -.2px; }
  .brand-text p { margin: 3px 0 0; color: var(--muted); font-size: 12px; }
  .title-note {
    color: #798296;
    font-size: 11.5px;
    white-space: nowrap;
  }

  .workspace {
    min-height: 0;
    display: grid;
    grid-template-columns: minmax(0, 1fr) 330px;
  }

  .editor-pane {
    min-width: 0;
    min-height: 0;
    display: flex;
    flex-direction: column;
    padding: 24px 26px 22px 28px;
    border-right: 1px solid var(--border-soft);
  }
  .pane-heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 10px;
  }
  .pane-heading h2,
  .control-pane h2 {
    margin: 0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .04em;
    text-transform: uppercase;
    color: #d8dce7;
  }
  .charcount { color: var(--muted); font-size: 12px; font-variant-numeric: tabular-nums; }
  textarea {
    width: 100%;
    flex: 1 1 auto;
    min-height: 260px;
    resize: none;
    padding: 18px 19px;
    border: 1px solid var(--border);
    border-radius: 8px;
    outline: none;
    background: var(--surface-2);
    color: var(--text);
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 1px 0 rgba(255,255,255,.018) inset;
  }
  textarea::placeholder { color: #646d80; }
  textarea:focus, select:focus {
    border-color: #6479dc;
    box-shadow: 0 0 0 2px rgba(111,134,255,.10);
  }

  .control-pane {
    min-height: 0;
    overflow-y: auto;
    padding: 24px 24px 22px;
    background: #13161f;
  }
  .control-pane > h2 { margin-bottom: 18px; }
  .control-group {
    padding: 17px;
    margin-bottom: 14px;
    border: 1px solid var(--border-soft);
    border-radius: 8px;
    background: var(--surface);
  }
  label {
    display: block;
    margin-bottom: 8px;
    color: #bfc5d2;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .055em;
    text-transform: uppercase;
  }
  select {
    width: 100%;
    height: 40px;
    padding: 0 36px 0 12px;
    appearance: none;
    border: 1px solid var(--border);
    border-radius: 7px;
    outline: none;
    color: var(--text);
    background-color: var(--surface-2);
    background-image:
      linear-gradient(45deg, transparent 50%, #8d96a9 50%),
      linear-gradient(135deg, #8d96a9 50%, transparent 50%);
    background-position: calc(100% - 16px) 17px, calc(100% - 11px) 17px;
    background-size: 5px 5px, 5px 5px;
    background-repeat: no-repeat;
    font-size: 13px;
  }
  .speed-wrap { margin-top: 15px; }

  #genBtn {
    width: 100%;
    height: 44px;
    margin: 2px 0 14px;
    border: 0;
    border-radius: 8px;
    color: #fff;
    background: linear-gradient(100deg, var(--accent), var(--accent-2));
    font-weight: 700;
    font-size: 13px;
    cursor: pointer;
    box-shadow: 0 7px 20px rgba(99,92,220,.18);
    transition: filter .15s ease, transform .15s ease;
  }
  #genBtn:hover { filter: brightness(1.08); transform: translateY(-1px); }
  #genBtn:active { transform: translateY(0); }
  #genBtn:disabled { cursor: wait; filter: saturate(.55) brightness(.78); transform: none; }

  .status-box {
    min-height: 42px;
    display: flex;
    align-items: center;
    padding: 0 12px;
    border: 1px solid var(--border-soft);
    border-radius: 7px;
    background: #10131b;
    color: var(--muted);
    font-size: 12px;
  }
  #status.working::before {
    content: "";
    width: 7px;
    height: 7px;
    flex: 0 0 auto;
    margin-right: 9px;
    border-radius: 50%;
    background: #a978ff;
    box-shadow: 0 0 0 0 rgba(169,120,255,.4);
    animation: pulse 1.2s infinite;
  }
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(169,120,255,.4); }
    70% { box-shadow: 0 0 0 7px rgba(169,120,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(169,120,255,0); }
  }

  #result:not(:empty) {
    margin-top: 14px;
    padding: 14px;
    border: 1px solid var(--border-soft);
    border-radius: 8px;
    background: var(--surface);
  }
  .result-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    color: var(--success);
    font-size: 12px;
    font-weight: 700;
  }
  audio { width: 100%; height: 36px; }
  a.download {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 36px;
    margin-top: 10px;
    border: 1px solid #3a4260;
    border-radius: 7px;
    color: #c5ceff;
    text-decoration: none;
    font-size: 12px;
    font-weight: 650;
    background: #151a28;
  }
  a.download:hover { background: #1a2030; color: #fff; }

  .footerbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    padding: 0 28px;
    border-top: 1px solid var(--border-soft);
    background: #12151d;
    color: #6f788b;
    font-size: 10.5px;
  }
  .footerbar .online::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 6px;
    margin-right: 7px;
    border-radius: 50%;
    background: #7488ff;
    vertical-align: 1px;
  }

  @media (max-width: 820px) {
    body { overflow: auto; }
    .app-shell { height: auto; min-height: 100vh; grid-template-rows: 66px auto 34px; }
    .workspace { grid-template-columns: 1fr; }
    .editor-pane { min-height: 500px; border-right: 0; border-bottom: 1px solid var(--border-soft); padding: 20px; }
    .control-pane { padding: 20px; }
    .titlebar { padding: 0 20px; }
    .title-note { display: none; }
    .footerbar { padding: 0 20px; }
  }
</style>
</head>
<body>
<div class="app-shell">
  <header class="titlebar">
    <div class="brand">
      <div class="app-icon" aria-hidden="true">
        <div class="wave"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
      </div>
      <div class="brand-text">
        <h1>Narration Generator</h1>
        <p>Long-form text to speech</p>
      </div>
    </div>
    <div class="title-note">Local utility · Internet required for voice generation</div>
  </header>

  <main class="workspace">
    <section class="editor-pane">
      <div class="pane-heading">
        <h2>Script</h2>
        <div class="charcount" id="charcount">0 characters</div>
      </div>
      <textarea id="text" placeholder="Paste or type your narration script here..."></textarea>
    </section>

    <aside class="control-pane">
      <h2>Narration Settings</h2>

      <div class="control-group">
        <label for="language">Language / Region</label>
        <select id="language"></select>

        <div class="speed-wrap">
          <label for="voice">Voice</label>
          <select id="voice"></select>
        </div>

        <div class="speed-wrap">
          <label for="rate">Speed</label>
          <select id="rate">
            <option value="-20%">Slower</option>
            <option value="+0%" selected>Normal</option>
            <option value="+15%">Faster</option>
          </select>
        </div>
      </div>

      <button id="genBtn" onclick="generate()">Generate Narration</button>

      <div class="status-box"><span id="status">Ready to generate.</span></div>
      <div id="result"></div>
    </aside>
  </main>

  <footer class="footerbar">
    <span>Narration Generator</span>
    <span class="online">Voice generation uses Microsoft Edge TTS</span>
  </footer>
</div>

<script>
const voiceCatalog = {voice_catalog};
const languageEl = document.getElementById('language');
const voiceEl = document.getElementById('voice');
const textEl = document.getElementById('text');
const charcount = document.getElementById('charcount');

function populateLanguages() {
  const locales = [];
  const seen = new Set();
  voiceCatalog.forEach(voice => {
    if (!seen.has(voice.locale)) {
      seen.add(voice.locale);
      locales.push({ locale: voice.locale, language: voice.language });
    }
  });

  languageEl.innerHTML = locales.map(item =>
    `<option value="${item.locale}">${item.language}</option>`
  ).join('');

  languageEl.value = seen.has('en-US') ? 'en-US' : (locales[0]?.locale || '');
  populateVoices();
}

function populateVoices() {
  const locale = languageEl.value;
  const matches = voiceCatalog.filter(voice => voice.locale === locale);
  voiceEl.innerHTML = matches.map(voice =>
    `<option value="${voice.code}">${voice.label}</option>`
  ).join('');

  if (locale === 'en-US' && matches.some(voice => voice.code === 'en-US-GuyNeural')) {
    voiceEl.value = 'en-US-GuyNeural';
  }
}

languageEl.addEventListener('change', populateVoices);
populateLanguages();

textEl.addEventListener('input', () => {
  charcount.textContent = textEl.value.length.toLocaleString() + ' characters';
});

async function generate() {
  const text = textEl.value.trim();
  const voice = document.getElementById('voice').value;
  const rate = document.getElementById('rate').value;
  const statusEl = document.getElementById('status');
  const resultEl = document.getElementById('result');
  const btn = document.getElementById('genBtn');

  if (!text) {
    statusEl.className = '';
    statusEl.textContent = 'Type or paste some text first.';
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Generating...';
  statusEl.className = 'working';
  statusEl.textContent = 'Generating narration. Long scripts may take a few minutes.';
  resultEl.innerHTML = '';

  try {
    const result = await window.pywebview.api.generate_audio(text, voice, rate);

    if (!result || !result.ok) {
      throw new Error(result?.error || 'Generation failed');
    }

    const binary = atob(result.audio_base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }

    const blob = new Blob([bytes], { type: 'audio/mpeg' });
    const url = URL.createObjectURL(blob);

    resultEl.innerHTML = `
      <div class="result-title"><span>Narration ready</span><span>MP3</span></div>
      <audio controls src="${url}"></audio>
      <a class="download" href="${url}" download="narration.mp3">Download MP3</a>
    `;

    statusEl.className = '';
    statusEl.textContent = 'Generation complete.';
  } catch (err) {
    statusEl.className = '';
    statusEl.textContent = 'Error: ' + err.message;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate Narration';
  }
}

// Desktop app: Python is called directly through pywebview.
</script>
</body>
</html>
"""


def render_page():
    catalog_json = json.dumps(get_voice_catalog(), ensure_ascii=False).replace("</", "<\\/")
    return PAGE.replace("{voice_catalog}", catalog_json)


class NarrationAPI:
    def generate_audio(self, text, voice, rate):
        text = (text or "").strip()
        voice = voice or "en-US-GuyNeural"
        rate = rate or "+0%"

        if not text:
            return {"ok": False, "error": "No text provided"}

        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

        try:
            async def run():
                communicate = edge_tts.Communicate(text, voice, rate=rate)
                await communicate.save(path)

            asyncio.run(run())

            with open(path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode("ascii")

            return {
                "ok": True,
                "audio_base64": audio_base64,
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": f"Generation failed: {exc}",
            }

        finally:
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    api = NarrationAPI()

    webview.create_window(
        "Narration Generator",
        html=render_page(),
        js_api=api,
        width=1100,
        height=760,
        min_size=(820, 620),
        resizable=True,
    )

    webview.start()
