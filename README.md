<div align="center">

# ⚡ SMD (Social Media Downloader)

### The Universal, Zero-Disk High-Speed Media Extraction Engine & Modern Web Suite
**Powered by [StdAPI](https://github.com/STD-DEEPANSHU/StdAPI) • Maintained by [TeamStdNetwork](https://github.com/TeamStdNetwork)**

<br/>

[![License: STD-PL-1.0](https://img.shields.io/badge/License-STD--PL--1.0-blue.svg?style=for-the-badge)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](#)
[![Powered by StdAPI](https://img.shields.io/badge/Engine-StdAPI%20v2.2-green.svg?style=for-the-badge)](https://github.com/STD-DEEPANSHU/StdAPI)
[![Platforms](https://img.shields.io/badge/Platforms-1800%2B%20Sites-purple.svg?style=for-the-badge)](#)

<br/>

> **SMD** is a world-class, privacy-first, lightning-fast social media downloader application. It allows seamless video, audio, and album downloads from Instagram, YouTube (up to 4K), TikTok (without watermark), Twitter/X, Pinterest, and 1,800+ other platforms using **Zero-Disk In-Memory Streaming**.

<br/>

[Key Features](#-key-features) • [Supported Platforms](#-supported-platforms) • [Quick Start](#-quick-start) • [API Reference](#-api-reference) • [License](#-license)

</div>

---

## 🚀 Key Features

- 🏎️ **Zero-Disk In-Memory Streaming:** Media is extracted and streamed directly without wasting temporary disk I/O, ensuring lightning-fast downloads and zero server clutter.
- 🎯 **No Watermark Extraction:** Download TikTok videos and Instagram Reels in crisp original resolution without watermarks.
- 🎧 **Smart Audio Extraction:** One-click conversion to high-bitrate MP3 (320kbps) with full ID3 metadata tags.
- 🛡️ **Stealth Browser Spoofing:** Employs real TLS/JA3 fingerprint spoofing and local cookie harvesting to bypass login walls, bot detectors, and IP throttling.
- 📱 **Modern Glassmorphic Web UI:** Clean, responsive, mobile-first interface with instant link detection, clipboard auto-paste, and media preview.
- 🔌 **REST API & Developer Ready:** Fully documented endpoints powered by FastAPI, ready to integrate into Telegram bots, Discord bots, or mobile apps.

---

## 🌐 Supported Platforms

| Platform | Supported Content | Max Resolution | Watermark Free |
| :--- | :--- | :--- | :---: |
| **Instagram** | Reels, Posts, Stories, Carousels, Audio | 1080p Original | ✅ |
| **YouTube** | Videos, Shorts, Playlists, Audio | Up to 4K UHD | ✅ |
| **TikTok** | Videos, Slideshows, Original Sound | 1080p HD | ✅ |
| **Twitter / X** | Videos, GIFs, High-Res Images | Source Quality | ✅ |
| **Pinterest** | Pins, Videos, High-Res Images | Source Quality | ✅ |
| **Facebook** | Public Videos, Reels | 1080p HD | ✅ |
| **1,800+ Others** | Supported via fallback `yt-dlp` engine | Source Quality | ✅ |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                   SMD Client (Web UI)                  │
└──────────────────────────┬─────────────────────────────┘
                           │ POST /api/extract (JSON)
                           ▼
┌────────────────────────────────────────────────────────┐
│                  FastAPI Backend Server                │
├──────────────────────────┬─────────────────────────────┤
│   Primary Engine         │   Fallback Stealth Engine   │
│   (StdAPI Cloud Nodes)   │   (StdEngine Local Cache)   │
└──────────────────────────┴─────────────────────────────┘
                           │
                           ▼
               Direct High-Speed CDN Stream
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/TeamStdNetwork/smd.git
cd smd
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux / macOS:
source venv/bin/activate

pip install -r backend/requirements.txt
```

### 3. Launch the Server
```bash
python backend/main.py
```
Open **`http://localhost:8000`** in your browser to access the Web UI and Swagger API Docs at **`http://localhost:8000/docs`**.

---

## 📡 API Reference

### 1. Extract Media Metadata & Download URL

**`POST /api/extract`**

#### Request Payload:
```json
{
  "url": "https://www.instagram.com/reel/C8xY9zABCDE/",
  "format": "mp4"
}
```

#### Response:
```json
{
  "success": true,
  "title": "Viral Summer Reel",
  "thumbnail": "https://...",
  "duration": 45,
  "platform": "instagram",
  "download_url": "https://...",
  "formats": [
    { "format_id": "hd", "resolution": "1080p", "url": "https://..." },
    { "format_id": "audio", "resolution": "MP3 320k", "url": "https://..." }
  ]
}
```

---

## ⚖️ License & Attribution

This project is licensed under the **STD Public License v1.0 (STD-PL-1.0)**.  
See the [LICENSE](LICENSE) file for complete terms and conditions.

- **Independent Integration:** Programs and websites that import or link with SMD's interfaces are **NOT** deemed derivative works and may be distributed under terms of your choosing (Section 3.a).
- **Core Modifications:** Any direct revisions made to the core engine must remain open under STD-PL-1.0.

---

<div align="center">
  Crafted with ❤️ by <b>TeamStdNetwork</b>
</div>
