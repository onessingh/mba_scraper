import os
import json
import datetime
from notifier import Notifier # type: ignore
from scraper import MBAScraper # type: ignore

# --- CONFIG ---
SCRAPER_KEY = os.environ.get("SCRAPER_KEY")
BACKEND_URL = os.environ.get("BACKEND_URL", "https://solmates-backend-w27e.onrender.com")

def reset_everything():
    print(f"[RESET]: Connecting to {BACKEND_URL}...")
    notifier = Notifier(BACKEND_URL, SCRAPER_KEY)
    
    # 1. Clear local memory
    memory_file = "synced_ids.json"
    if os.path.exists(memory_file):
        with open(memory_file, 'w') as f:
            f.write("[]")
        print(f"[RESET]: Cleared local memory file '{memory_file}'")
    
    # 2. Clear backend blacklist
    notifier.clear_blacklist()

    # 2. Delete all backend items for all semesters
    semesters = ["0", "1", "2", "3", "4"]
    total_deleted = 0
    
    for sem in semesters:
        print(f"[RESET]: Clearing Semester {sem}...")
        while True:
            items = notifier.get_from_website(sem)
            if not items:
                print(f"  [✔]: Semester {sem} is empty.")
                break
            
            print(f"  - Found {len(items)} items. Deleting batch...")
            deleted_in_batch = 0
            for item in items:
                item_id = item.get('_id') or item.get('id')
                if item_id:
                    if notifier.delete_from_website(sem, item_id):
                        deleted_in_batch += 1 # type: ignore
                        total_deleted += 1 # type: ignore
            
            if deleted_in_batch == 0:
                print("  [!] Warning: Found items but could not delete them. Breaking to avoid infinite loop.")
                break
            print(f"  - Batch complete ({deleted_in_batch} deleted). Re-checking...")

    print(f"\n[SUCCESS]: Reset complete. Total {total_deleted} items deleted from backend.")
    print("[INFO]: Next time you run the scraper, it will re-add everything from scratch.")

if __name__ == "__main__":
    reset_everything()
