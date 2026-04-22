import asyncio
import time
import os
import sqlite3
import datetime
import sys
import re
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Optional, Any, Dict # Added typing imports

try:
    import requests # type: ignore
except ImportError:
    pass

try:
    from scraper import MBAScraper # type: ignore
    from database import ScraperDatabase # type: ignore
    from notifier import Notifier # type: ignore
except ImportError:
    pass

# Tiny Health Check Server for Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Scraper is Alive")
    def log_message(self, format, *args): return # Silence logs

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"[HEALTH]: Started on port {port}")
    server.serve_forever()

async def job(days_back: int = 15, targets: Optional[List[str]] = None, mode: str = "all", allow_deletions: bool = True):
    """
    Main job function that runs the scraper and syncs with the backend.
    """
    # PRODUCTION UNIFIED CONFIGURATION
    API_URL: str = os.environ.get("BACKEND_URL", "https://solmates-backend-w27e.onrender.com")
    API_KEY: str = os.environ.get("SCRAPER_KEY", "")
    
    scraper = MBAScraper(target_mode=mode)
    db = ScraperDatabase()
    notifier = Notifier(api_url=API_URL, scraper_key=API_KEY)
    
    print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [JOB]: Starting MBA Scraper | Mode: {mode} | Deletions: {allow_deletions}")
    try:
        results: List[Dict[str, Any]] = await scraper.run(days_back=days_back, mode=mode, targets=targets)
        results = results if results is not None else []
        print(f"[JOB]: Found {len(results)} possible MBA items.")
        
        # Sync logic (BULK SYNC) - Optimized for accuracy and deletions
        scraper.sync_results(results, notifier, "synced_ids.json", allow_deletions=allow_deletions)
                    
        print(f"[JOB]: Finished Scraper Job.")
    except Exception as e:
        import traceback
        print(f"[ERROR]: Job failed: {e}")
        print(traceback.format_exc())

def keep_alive():
    """Self-ping to prevent Render sleep (Free Tier)"""
    url = os.environ.get("SELF_URL", "https://mba-scraper.onrender.com")
    while True:
        try:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [KEEP-ALIVE]: Pinging {url}...")
            requests.get(url, timeout=10) # type: ignore
        except Exception as e:
            print(f"[KEEP-ALIVE][ERROR]: {e}")
        time.sleep(600) # Ping every 10 minutes

async def main():
    # Start Health Check Server in a separate thread
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Start Keep-Alive Pinger in a separate thread
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()

    run_once = "--once" in sys.argv
    if run_once:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running One-Shot Comprehensive Job...")
        await job(mode="all")
        return

    print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] MBA Scraper Service Initializing...")
    pulse_index: int = 0
    
    while True:
        try:
            p_idx: int = int(pulse_index)
            # Every 60 minutes (6th pulse of 10 min each), run EVERYTHING including classes
            if p_idx % 6 == 0:
                print(f"\n[PULSE {p_idx}]: Triggering 1-HOUR COMPREHENSIVE scan (Website + Classes)...")
                await job(mode="all") 
            else:
                # Every 10 minutes, run only Website and Notices scan
                print(f"\n[PULSE {p_idx}]: Triggering 10-MINUTE WEBSITE & NOTICES scan...")
                await job(mode="website")
            
            pulse_index = int(pulse_index) + 1 # type: ignore
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [SLEEP]: Pulse complete. Next pulse in 600 seconds...")
            await asyncio.sleep(600)
        except Exception as e:
            print(f"[MAIN][ERROR]: Loop error: {e}")
            await asyncio.sleep(60)

def main_job(mode="all", allow_deletions: bool = True):
    """
    Synchronous wrapper for the job function, easily callable from external scripts.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        # If we are already in an event loop (rare but possible)
        try:
            import nest_asyncio # type: ignore
            nest_asyncio.apply()
            loop.create_task(job(mode=mode, allow_deletions=allow_deletions))
        except ImportError:
            print("[WARN]: nest_asyncio not found. Task might not run correctly inside existing loop.")
    else:
        loop.run_until_complete(job(mode=mode, allow_deletions=allow_deletions))

if __name__ == "__main__":
    asyncio.run(main())
