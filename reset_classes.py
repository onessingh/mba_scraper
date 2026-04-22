#!/usr/bin/env python3
"""
RESET SCRIPT: Clears all live-classes data for Sem 1, 2, 3, 4 from the backend.
Run this ONCE before running scraper.py to ensure fresh sync.
Usage: python reset_classes.py
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "").rstrip("/")
SCRAPER_KEY = os.environ.get("SCRAPER_KEY", "")

if not BACKEND_URL or not SCRAPER_KEY:
    print("[ERROR]: BACKEND_URL or SCRAPER_KEY missing in .env!")
    print("  Set them in your .env file:")
    print("  BACKEND_URL=https://your-backend.onrender.com")
    print("  SCRAPER_KEY=your_scraper_key")
    exit(1)

headers = {
    "x-scraper-key": SCRAPER_KEY,
    "Content-Type": "application/json"
}

print(f"[RESET]: Backend → {BACKEND_URL}")
print("[RESET]: Starting live-classes wipe for Sem 0, 1, 2, 3, 4...\n")

for category in ["live-classes", "notifications"]:
    for sem in ["0", "1", "2", "3", "4"]:
        try:
            # Bulk sync with empty list = clears all items for this sem
            url = f"{BACKEND_URL}/api/sol/sync-bulk/{category}/{sem}"
            payload = {"items": [], "allow_deletions": True}
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if r.status_code == 200:
                data = r.json()
                print(f"  [✅ CLEARED]: {category} Sem {sem} → {data}")
            else:
                print(f"  [❌ FAILED]: {category} Sem {sem} → HTTP {r.status_code}: {r.text[:100]}")
        except Exception as e:
            print(f"  [❌ ERROR]: {category} Sem {sem} → {e}")

print("\n[RESET]: Done! Now run: python scraper.py")
print("[RESET]: Classes and notifications will be re-populated from fresh scrape.")
