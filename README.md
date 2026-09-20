# 🎙️ Narration Generator (Text To Speech/TTS)

A simple, portable Windows narration generator built for creators, developers, educators, and anyone who needs clean voice narration without a complicated workflow.

Paste your text, select a language, regional voice, and speed, then generate, preview, and save your narration as an `.mp3` file.

No account or subscription is required to use the application.

---

## ⚡ Distribution Channels & Architecture

The Narration Generator is provided in two forms: a ready-to-use Windows executable and a source-available developer version.

### 🚀 1. Standalone Windows Binary (.exe)

- **No Installer Required:** Download the executable and run it directly.
- **Portable:** The application does not need to be formally installed on Windows.
- **No Local Python Setup Required:** The standalone executable includes what it needs to run the application.
- **Simple Removal:** If you no longer want the program, simply delete the executable.

An active internet connection is still required when generating narration because voice generation uses an online text-to-speech service.

### 📂 2. Developer Source Files

The source code is included for transparency, inspection, learning, testing, and personal modification under the included project license.

The source files include:

- Core Python application logic (`narrate_web.py`)
- Desktop launcher and setup scripts
- Python dependency configuration (`requirements.txt`)
- Project license
- Third-party notices and acknowledgments

---

## ✨ Features & Core Capabilities

- **🌐 Multiple Languages & Regions:** Choose from supported languages and regional voice options.
- **🎙️ Multiple Voice Profiles:** Browse available voices and experiment until you find the voice that fits your project.
- **🎛️ Speed Controls:** Adjust narration speed before generating audio.
- **📺 Built-In Audio Preview:** Listen to generated narration directly inside the application before saving it.
- **💾 MP3 Export:** Save generated narration directly to your computer using the Windows Save As dialog.
- **🖥️ Portable Windows Application:** Run the standalone executable without a traditional installer.
- **👤 No Account Required:** The application does not require account registration or login.
- **🧩 Simple Interface:** Designed around a straightforward workflow without unnecessary menus, dashboards, or setup steps.

---

## 🖥️ Verified Performance & Hardware Test

The Narration Generator itself does not impose a fixed text-length limit.

Practical generation limits and processing times can vary depending on system resources, internet connection quality, selected voice, narration speed, and the underlying text-to-speech service.

The following test provides one real-world example of long-form performance.

### 📋 Test System Configuration

- **Processor:** Intel Core i7-1255U (10 Cores / 12 Threads)
- **Memory:** 16 GB RAM
- **Storage:** NVMe SSD
- **Operating System:** Windows 11

### 📊 Long-Form Test Results

- **Script Length:** 18,644 characters (~3,700 words)
- **Selected Voice:** Brian — US male voice
- **Speed:** Normal
- **Output Audio Duration:** **21 minutes, 34 seconds**
- **Generation Time:** Approximately **5 minutes**
- **Approximate Processing Rate:** Around **4.3× faster than the finished narration's playback length**

This was an informal real-world test rather than a controlled benchmark.

Performance may be faster or slower on different systems or network connections.

---

## 🛠️ Requirements & Dependencies

- **Internet Connection:** An active internet connection is required during narration generation.
- **Windows:** The standalone executable is packaged as a Windows desktop application.
- **Source Version:** Running directly from source requires Python and the packages listed in `requirements.txt`.

The project uses technologies including:

- Python
- pywebview
- Edge TTS
- Microsoft speech and voice technology

---

## ⚠️ Practical Limitations

Very long scripts may take several minutes to generate.

The application itself does not intentionally restrict narration length, but extremely large generations may ultimately be affected by:

- Available system resources
- Internet connection quality
- Network interruptions
- Voice service availability
- Limits or behavior of the underlying text-to-speech service

Generation speed may vary between computers and internet connections.

---

## 📜 Intellectual Property & Third-Party Notices

This project is **source-available** under the included custom license.

The developer does not claim ownership of Python, pywebview, Edge TTS, Microsoft voices, Microsoft speech technology, third-party libraries, services, trademarks, or other third-party technologies used by or accessed through the application.

All third-party technologies, voices, libraries, services, and trademarks remain the property of their respective owners and are subject to their own licenses, policies, and terms.

The project license applies only to the original application code, interface, scripts, documentation, project structure, and other original project material.

See the accompanying `THIRD_PARTY_NOTICES.md` file for additional acknowledgments and information.

---

## 💜 Acknowledgments

A sincere thank you to the developers, maintainers, contributors, and communities behind Python, pywebview, Edge TTS, Microsoft speech technologies, and the tools that make this project possible.

The available voices and supporting technologies make it possible to create useful narration for educational videos, explainers, documentaries, mystery content, technology topics, science, space, and many other creative projects.

This project exists because other developers created powerful tools, documented them, maintained them, and made it possible for others to build useful things with them.

Thank you to everyone who created, documented, maintained, and improved the technologies this project depends on. 💜

---

## 📂 Source Files & Inspection (Transparent, Not Public Domain)

The raw source code is fully exposed inside this repository for transparency, security inspection, personal modification, and educational learning.

**Usage Restrictions:**

* **Transparency First:** You are encouraged to review the `.py` files to understand how the application works and inspect the source used to build the compiled executable.

* **No Redistribution as Your Own Product:** You may not copy, repackage, rebrand, sell, redistribute, or publish this software, its source files, or compiled versions as your own standalone product.

* **Personal Customization:** You are welcome to modify your own local copy for personal, educational, testing, or development use.

* **Third-Party Technology:** These restrictions apply only to the original project material. Third-party libraries, voices, frameworks, and technologies remain subject to their own licenses and terms.

See the included `LICENSE` file for the full usage terms.
