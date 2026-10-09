# pyre-ignore-all-errors
# pyre-unsafe
# type: ignore
"""
reset_and_sync.py — Ek baar manually chalao:
1. Backend se sab kuch delete karo (semesters 0,1,2,3,4)
2. synced_ids.json clear karo
3. Fresh scrape karo
4. Sab kuch dobara sync karo (notifications jayengi)

Usage:
  python reset_and_sync.py
"""

import os
import sys

# Add current directory to path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import json
import time

try:
    from notifier import Notifier # type: ignore # pyre-ignore[21]
except ImportError:
    print("[ERROR]: notifier.py nahi mila. Is script ko mba_scraper/ folder mein se chalao.")
    sys.exit(1)

try:
    from scraper import MBAScraper # type: ignore # pyre-ignore[21]
except ImportError:
    print("[ERROR]: scraper.py nahi mila.")
    sys.exit(1)

BACKEND_URL = os.environ.get("BACKEND_URL", "https://solmates-backend-f9rl.onrender.com")
SCRAPER_KEY = os.environ.get("SCRAPER_KEY", "")
SYNCED_FILE = "synced_ids.json"
SEMESTERS   = ["0", "1", "2", "3", "4"]


def delete_all(notifier: Notifier):
    """Backend se notifications aur live-classes ki saari entries ek saath delete karo."""
    print("\n" + "="*50)
    print("[RESET]: Step 1 — Backend se sab delete kar rahe hain (ATOMIC)...")
    print("="*50)

    # Atomic clear for both categories
    n_ok = notifier.clear_category("notifications")
    l_ok = notifier.clear_category("live-classes")
    b_ok = notifier.clear_blacklist()

    if n_ok and l_ok and b_ok:
        print("\n  ✅ Backend fully reset (Notifications, Live Classes, and Blacklist).")
    else:
        print("\n  ⚠️  Kuch operations fail hue. Check backend logs.")


def clear_memory():
    """synced_ids.json and hash caches reset karo taaki sab kuch dobara sync ho."""
    print("\n" + "="*50)
    print("[RESET]: Step 2 — Local memory & hash caches clear kar rahe hain...")
    print("="*50)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, SYNCED_FILE), "w") as f:
        json.dump([], f)

    for h_file in ["synced_hashes.json", "payload_hashes.json"]:
        h_path = os.path.join(base_dir, h_file)
        if os.path.exists(h_path):
            os.remove(h_path)
            print(f"  ✅ Removed {h_file}")

    print(f"  ✅ {SYNCED_FILE} and hash caches cleared.")


async def fresh_scrape_and_sync(notifier: Notifier):
    """Fresh scrape karo aur sab sync karo."""
    print("\n" + "="*50)
    print("[RESET]: Step 3 — Fresh scrape + sync...")
    print("="*50)

    scraper = MBAScraper(target_mode="all", force_sync=True)
    results = await scraper.run(mode="all")

    print(f"\n[RESET]: {len(results)} items scraped.")

    if results:
        scraper.sync_results(results, notifier, SYNCED_FILE)
        print("\n[RESET]: ✅ Sync complete — notifications bhej di gayi hain!")
    else:
        print("\n[RESET]: ⚠️  Koi item nahi mila. Backend empty rahega.")

    return results


async def main():
    print("\n" + "="*50)
    print("  SOL MBA — FULL RESET & FRESH SYNC")
    print("="*50)
    print(f"  Backend: {BACKEND_URL}")
    print(f"  Key:     {'*' * len(SCRAPER_KEY) if SCRAPER_KEY else '❌ NOT SET'}")
    print("="*50)

    if not SCRAPER_KEY:
        print("\n[ERROR]: SCRAPER_KEY environment variable set nahi hai!")
        print("  Run: export SCRAPER_KEY=your_key")
        sys.exit(1)

    notifier = Notifier(api_url=BACKEND_URL, scraper_key=SCRAPER_KEY)

    # Confirm karo
    print("\n⚠️  WARNING: Yeh sab kuch delete karke fresh start karega.")
    print("   Sab purani notifications delete hongi aur dobara bhejegi jayengi.")
    confirm = input("\n   Confirm? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("[RESET]: Cancelled.")
        sys.exit(0)

    # Step 1: Delete all
    delete_all(notifier)

    # Step 2: Clear memory
    clear_memory()

    # Step 3: Fresh scrape + sync
    await fresh_scrape_and_sync(notifier)

    print("\n" + "="*50)
    print("  ✅ RESET COMPLETE!")
    print("  Ab se scraper normal tarah kaam karega.")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(main())
