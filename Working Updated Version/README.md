# Narration Generator — Working Updated Version

This folder is a **separate, updated copy** of the Narration Generator. The original repository files can remain untouched.

## Windows quick start

1. Download this folder (or the ZIP) and extract it.
2. Run `1. Setup (run once).bat` to install Python dependencies.
3. Run `2. Start Narration Tool.bat` to launch the browser-based narrator.
4. Enter text, select a voice and speed, generate, and download the MP3.

Python and pip must be installed and available in PATH. The app runs locally at `http://127.0.0.1:5050/`, but speech synthesis requires an internet connection.

## October 2026 speech service compatibility fix

The `edge-tts` library version 7.2.8 used the legacy Microsoft Edge Read Aloud WebSocket address, which began returning HTTP 403. This version locally overrides `edge_tts.communicate.WSS_URL` with the newer speech endpoint reported by the community. It also retries **once** after three seconds on an HTTP 429 rate limit. The remaining narrator UI and MP3 workflow are unchanged.

This is a community-reported, unofficial workaround, not a Microsoft-supported API. It was reported working in a local user test, but may stop working if the service changes again. Do not assume third-party use or commercial rights based on a successful connection; review Microsoft's applicable terms.

The ZIP includes `edge-tts==7.2.8`, the version against which the workaround was tested. Existing repository `LICENSE` and `THIRD_PARTY_NOTICES.md` should be retained; verify attribution before redistributing.

**Note:** Running this copy closes an existing local Narration Generator instance on port 5050, if one is active.
