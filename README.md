# 🎙️ Narration Generator (Text To Speech/TTS)

A simple, portable Windows narration generator built for creators, developers, educators, and anyone who needs clean voice narration without a complicated workflow.

Paste your text, select an available voice and speed, then generate, preview, and save your narration as an `.mp3` file.

No account or subscription is required to use the application.

---

## 🚨 October 2026 Update — Temporary Edge TTS Compatibility Fix

**Important: The original Windows EXE has NOT been updated.**

In October 2026, users began reporting HTTP 403 WebSocket handshake errors affecting the `edge-tts` library and Microsoft's Edge Read Aloud speech service.

These connection errors can prevent Narration Generator from generating audio, even when the application itself opens and functions normally.

A temporary, application-level workaround has been tested successfully and is now available in the repository's **`Working Updated Version`** folder.

### ✅ What Has Been Updated

The updated Python version:

- Uses the newer `api.msedgeservices.com` speech synthesis endpoint instead of the older `speech.platform.bing.com` endpoint.
- Applies the endpoint change through `edge_tts.communicate.WSS_URL`.
- Retains the existing trusted client token.
- Includes one bounded retry with a 3-second delay for HTTP 429 rate-limit responses.
- Preserves the existing narration interface, voice selection, speed controls, and MP3 generation.

**Initial test result:** Narration generation was successfully restored on Windows without a VPN or proxy.

The HTTP 429 retry has been implemented but has not been separately verified during a rate-limit event.

### ⚠️ What Has NOT Been Updated

- The original compiled Windows `.exe` remains unchanged.
- The original repository source files remain available for reference.
- The temporary workaround is not a permanent fix to the upstream `edge-tts` library.
- Compatibility may change again if Microsoft modifies its speech service.

**If your existing EXE is encountering HTTP 403 errors, use the updated Python version described below for now.**

This workaround is based on findings shared by contributors in the [edge-tts GitHub issue #490](https://github.com/rany2/edge-tts/issues/490).

---

## 🚀 Quick Start — Working Updated Version

The temporary working version runs directly from Python and does not require compiling or packaging an EXE.

### 📥 Step 1 — Download the Updated Files

Open the **`Working Updated Version`** folder in this repository.

Download the updated version and extract the files into a folder on your Windows computer.

Keep the Python file, batch launchers, and `requirements.txt` together.

### 🛠️ Step 2 — Run Setup Once

Make sure Python is installed on your computer and available from Command Prompt.

Double-click:

`1. Setup (run once).bat`

This installs the Python packages required by the updated narration generator.

An internet connection is needed to install dependencies.

### ▶️ Step 3 — Start Narration Generator

Double-click:

`2. Start Narration Tool.bat`

The launcher starts the local Python application.

Your browser should open the Narration Generator interface.

Keep the launcher or Command Prompt window running while using the tool.

### 🎙️ Step 4 — Generate Your Narration

1. Paste or type your narration script.
2. Select an available voice.
3. Choose your preferred narration speed.
4. Click **Generate Narration**.
5. Preview the resulting audio and download the MP3.

**For future sessions:** You normally only need to run **`2. Start Narration Tool.bat`**. The setup step is not required every time.

The updated source version runs locally, but speech generation still requires an active internet connection to Microsoft's online speech service.

---

## ⚡ Distribution Channels & Architecture

Narration Generator has been provided as a standalone Windows executable and a source-available developer version.

An additional updated Python folder is now available as a temporary compatibility workaround.

### 🖥️ 1. Standalone Windows Binary (.exe) — Not Yet Updated

- **No Installer Required:** The original executable can be downloaded and launched directly.
- **Portable:** It does not require a traditional Windows installation.
- **No Local Python Setup Required:** The compiled executable includes its required application runtime.
- **Simple Removal:** The portable application can be removed by deleting its executable.

**Current limitation:** The existing EXE has not received the October 2026 Edge TTS endpoint workaround and may encounter HTTP 403 errors.

Do not assume the EXE includes the updated speech connection.

### 📂 2. Original Developer Source Files

The original source code remains available for transparency, inspection, learning, testing, and permitted personal modification under the included project license.

These files reflect the earlier implementation and may still use the previous speech endpoint.

### ✅ 3. Working Updated Version — Temporary Fix

The **`Working Updated Version`** folder contains the updated Python implementation and simple setup and launch scripts.

This is currently the version to try if the older application is encountering the HTTP 403 connection error.

It does **not** replace or update the existing Windows EXE.

---

## ✨ Features & Core Capabilities

Features vary slightly between the original packaged application and the updated Python/browser version.

- **🌐 Multiple Voice Options:** Select from the English regional voices available in the updated source version.
- **🎙️ Voice Profiles:** Experiment with supported voices to find a suitable narration style.
- **🎛️ Speed Controls:** Adjust narration speed before generating audio.
- **📺 Built-In Audio Preview:** Listen to generated narration before saving it.
- **💾 MP3 Export:** Download generated audio to your computer.
- **🖥️ Portable Windows EXE:** The original compiled version can run without a separate Python installation, but has not yet received the compatibility update.
- **👤 No Account Required:** No application account registration or login.
- **🧩 Simple Interface:** Straightforward narration generation without complicated menus or dashboards.

---

## 🖥️ Previously Verified Performance & Hardware Test

The Narration Generator application does not impose a fixed text-length limit.

Practical generation limits and processing times can vary depending on system resources, internet connection quality, selected voice, narration speed, and the underlying text-to-speech service.

The following results are from an **earlier long-form test of the original application**, not a new benchmark of the October 2026 workaround.

### 📋 Test System Configuration

- **Processor:** Intel Core i7-1255U (10 Cores / 12 Threads)
- **Memory:** 16 GB RAM
- **Storage:** NVMe SSD
- **Operating System:** Windows 11

### 📊 Long-Form Test Results

- **Script Length:** 18,644 characters (approximately 3,700 words)
- **Selected Voice:** Brian — US male voice
- **Speed:** Normal
- **Output Audio Duration:** **21 minutes, 34 seconds**
- **Generation Time:** Approximately **5 minutes**
- **Approximate Processing Rate:** Around **4.3× faster than the finished narration's playback length**

This was an informal real-world test rather than a controlled benchmark.

Performance may be faster or slower on different systems or network connections.

These results should not be interpreted as verified performance for the newly updated Python version.

---

## 🛠️ Requirements & Dependencies

### Original Windows EXE

- Compatible Windows environment
- Active internet connection for narration generation
- No separate local Python installation required

### Working Updated Version

- Windows
- Python
- Python dependencies installed using the supplied setup script
- Active internet connection for narration generation

Technologies used across the project versions include:

- Python
- Flask
- pywebview (original desktop application)
- Edge TTS
- Microsoft speech and voice technology

The updated Python version uses Flask to serve its interface locally in a browser.

---

## ⚠️ Practical Limitations & Service Availability

Narration Generator depends on an external online speech service.

The application itself does not intentionally restrict narration length, but very large generations may be affected by:

- System resources
- Internet connection quality
- Network interruptions
- Voice service availability
- Service rate limits
- Changes to Microsoft's speech infrastructure

The October 2026 workaround addresses the connection problem observed during initial testing, but continued compatibility is not guaranteed.

The Edge TTS connection is based on an unofficial interface and may change without notice.

For the latest upstream developments, refer to the [edge-tts project](https://github.com/rany2/edge-tts).

---

## 📜 Intellectual Property & Third-Party Notices

This project is **source-available** under the included custom license.

The developer does not claim ownership of Python, Flask, pywebview, Edge TTS, Microsoft voices, Microsoft speech technology, third-party libraries, services, trademarks, or other third-party technologies used by or accessed through the application.

All third-party technologies, voices, libraries, services, and trademarks remain the property of their respective owners and are subject to their own licenses, policies, and terms.

The project license applies only to the original application code, interface, scripts, documentation, project structure, and other original project material.

See the accompanying `THIRD_PARTY_NOTICES.md` file for additional acknowledgments and information.

Use of Microsoft's speech services remains subject to any applicable Microsoft terms and policies.

---

## 💜 Acknowledgments

A sincere thank you to the developers, maintainers, contributors, and communities behind Python, Flask, pywebview, Edge TTS, Microsoft speech technologies, and the tools that make this project possible.

Special thanks to the developers contributing findings and workarounds to [edge-tts issue #490](https://github.com/rany2/edge-tts/issues/490).

Their shared troubleshooting made it possible to test and apply the temporary October 2026 connection workaround.

The available voices and supporting technologies make it possible to create useful narration for educational videos, explainers, documentaries, mystery content, technology topics, science, space, and many other creative projects.

This project exists because other developers created powerful tools, documented them, maintained them, and made it possible for others to build useful things with them.

Thank you to everyone who created, documented, maintained, shared, and improved the technologies this project depends on. 💜

---

## 📂 Source Files & Inspection (Transparent, Not Public Domain)

The raw source code is provided in this repository for transparency, security inspection, personal modification, and educational learning.

**Usage Restrictions:**

- **Transparency First:** You are encouraged to review the `.py` files to understand how the application works and inspect the available source.

- **No Redistribution as Your Own Product:** You may not copy, repackage, rebrand, sell, redistribute, or publish this software, its source files, or compiled versions as your own standalone product.

- **Personal Customization:** You are welcome to modify your own local copy for personal, educational, testing, or development use.

- **Third-Party Technology:** These restrictions apply only to the original project material. Third-party libraries, voices, frameworks, and technologies remain subject to their own licenses and terms.

See the included `LICENSE` file for the full usage terms.

---

**Current status:** The updated Python narration generator has passed an initial speech generation test. The original Windows EXE remains unchanged and has **not yet been updated** with the October 2026 workaround.
