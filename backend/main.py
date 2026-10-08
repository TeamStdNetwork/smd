import re
import time
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl

# Import StdAPI media engine
try:
    from stdapi import media, StdEngine
except ImportError:
    media = None
    StdEngine = None

app = FastAPI(
    title="SMD - Social Media Downloader API",
    description="Universal, Zero-Disk High-Speed Media Downloader powered by StdAPI",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize local fallback engine if available
local_engine = StdEngine(use_cache=True) if StdEngine else None

# In-memory simple cache {url_hash: (timestamp, data)}
CACHE: Dict[str, tuple[float, Dict[str, Any]]] = {}
CACHE_TTL = 3600  # 1 hour cache

class ExtractRequest(BaseModel):
    url: str
    format: Optional[str] = "mp4"

def detect_platform(url: str) -> str:
    lower = url.lower()
    if "instagram.com" in lower:
        return "Instagram"
    elif "youtube.com" in lower or "youtu.be" in lower:
        return "YouTube"
    elif "tiktok.com" in lower:
        return "TikTok"
    elif "twitter.com" in lower or "x.com" in lower:
        return "Twitter / X"
    elif "pinterest.com" in lower or "pin.it" in lower:
        return "Pinterest"
    elif "facebook.com" in lower or "fb.watch" in lower:
        return "Facebook"
    elif "reddit.com" in lower:
        return "Reddit"
    return "Universal"

@app.post("/api/extract")
async def extract_media(payload: ExtractRequest):
    url = payload.url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Invalid URL. Please enter a valid http/https URL.")

    # Check Cache
    now = time.time()
    cache_key = f"{url}_{payload.format}"
    if cache_key in CACHE:
        cached_time, cached_data = CACHE[cache_key]
        if now - cached_time < CACHE_TTL:
            return cached_data

    platform = detect_platform(url)

    # 1. Primary extraction via StdAPI Cloud SDK
    if media is not None:
        try:
            res = await media.download(url=url, format=payload.format)
            if res and getattr(res, "download_url", None):
                response_data = {
                    "success": True,
                    "platform": platform,
                    "title": getattr(res, "title", f"{platform} Media"),
                    "thumbnail": getattr(res, "thumbnail", None),
                    "duration": getattr(res, "duration", None),
                    "download_url": getattr(res, "download_url", None),
                    "formats": getattr(res, "formats", []),
                    "quality": getattr(res, "quality", "HD"),
                    "cached": False
                }
                CACHE[cache_key] = (now, response_data)
                return response_data
        except Exception:
            pass  # Fall through to local engine

    # 2. Fallback to Local StdEngine (yt-dlp wrapper with stealth spoofing)
    if local_engine is not None:
        try:
            local_res = await local_engine.extract(url)
            if local_res:
                formats = local_res.get("formats", [])
                best_url = local_res.get("url") or (formats[0]["url"] if formats else None)
                response_data = {
                    "success": True,
                    "platform": platform,
                    "title": local_res.get("title", f"{platform} Media"),
                    "thumbnail": local_res.get("thumbnail"),
                    "duration": local_res.get("duration"),
                    "download_url": best_url,
                    "formats": formats,
                    "quality": "Best",
                    "cached": False
                }
                CACHE[cache_key] = (now, response_data)
                return response_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract media: {str(e)}")

    raise HTTPException(status_code=500, detail="Extraction engine not available. Please verify stdapi installation.")

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "engine": "StdAPI v2.2",
        "license": "STD-PL-1.0",
        "cache_entries": len(CACHE)
    }

# Mount Frontend static files
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

    @app.get("/")
    async def serve_index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "SMD API is active. Frontend index.html not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
