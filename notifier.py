# pyre-ignore-all-errors
# pyre-unsafe
# type: ignore
try:
    import requests # type: ignore
except ImportError:
    pass
import json

class Notifier:
    def __init__(self, api_url, scraper_key=None, ultra_msg_token=None, ultra_msg_instance=None):
        self.website_api_url = api_url.rstrip('/')
        self.scraper_key = scraper_key
        self.ultra_msg_token = ultra_msg_token
        self.ultra_msg_instance = ultra_msg_instance

    def send_whatsapp_alert(self, message):
        """
        Placeholder for UltraMsg/Twilio WhatsApp alert.
        In a real scenario, you would use requests.post to the UltraMsg API.
        """
        print(f"[WHATSAPP ALERT]: {message}")
        if self.ultra_msg_token and self.ultra_msg_instance:
            # url = f"https://api.ultramsg.com/{self.ultra_msg_instance}/messages/chat"
            # payload = {
            #     "token": self.ultra_msg_token,
            #     "to": "GROUP_ID",
            #     "body": message
            # }
            # requests.post(url, data=payload)
            pass

    def _request_with_retry(self, method, url, max_retries=3, **kwargs):
        """Generic request wrapper with basic retry logic"""
        import time
        for i in range(max_retries):
            try:
                # Optimized timeout for Bulk Sync operations
                current_timeout = kwargs.pop('timeout', 60)
                response = requests.request(method, url, timeout=current_timeout, **kwargs) # type: ignore
                # Success cases: 200/201 (Created), 204 (No Content), 404 (Not Found/Deleted), 409 (Conflict/Exists)
                if response.status_code in [200, 201, 204, 404, 409]:
                    return response
                print(f"[API][RETRY {i+1}]: {method} {url} returned {response.status_code}")
            except Exception as e:
                print(f"[API][RETRY {i+1}]: {method} {url} failed: {e}")
            time.sleep(2 * (i + 1)) # Exponential backoff
        return None

    def sync_to_website(self, notice_data):
        url = f"{self.website_api_url}/api/sol/notifications/{notice_data['semester']}"
        payload = {
            "title": notice_data['title'],
            "link": notice_data['link'],
            "date": notice_data['date'],
            "description": notice_data.get('description', '')
        }
        headers = {"Content-Type": "application/json", "x-scraper-key": self.scraper_key}
        resp = self._request_with_retry("POST", url, json=payload, headers=headers)
        
        if resp is not None:
            status = resp.status_code
            print(f"  [API]: POST {url} | Result: {status}")
            # Success if 201 (Created) or 409 (Conflict = Already exists)
            return status in [201, 409]
        else:
            print(f"  [API]: POST {url} | Result: FAILED (No response from backend)")
            return False

    def bulk_sync_to_website(self, category, semester, items, allow_deletions=True):
        """Bulk Sync: Replaces an entire semester's data in one transaction."""
        sync_url = f"{self.website_api_url}/api/sol/sync-bulk/{category}/{semester}"
        
        # Add deletion flag to URL
        if not allow_deletions:
            sync_url += "?allowDeletions=false"
            
        headers = {"Content-Type": "application/json", "x-scraper-key": self.scraper_key}
        
        print(f"  [API]: BULK SYNC {category} Sem {semester} ({len(items)} items) | Deletions: {allow_deletions}")
        payload = {"items": items}
        resp = self._request_with_retry("POST", sync_url, json=payload, headers=headers)
        
        if resp and resp.status_code == 200:
            print(f"  [✅ OK]: Bulk sync successful for {category} Sem {semester}.")
            return True
        else:
            print(f"  [❌ FAILED]: Bulk sync failed (Status: {resp.status_code if resp else 'No Response'})")
            return False

    def update_on_website(self, semester, item_id, notice_data):
        url = f"{self.website_api_url}/api/sol/notifications/{semester}/{item_id}"
        payload = {
            "title": notice_data['title'],
            "link": notice_data['link'],
            "date": notice_data['date'],
            "description": notice_data.get('description', '')
        }
        headers = {"Content-Type": "application/json", "x-scraper-key": self.scraper_key}
        resp = self._request_with_retry("PUT", url, json=payload, headers=headers)
        return resp is not None and resp.status_code == 200

    def delete_from_website(self, semester, item_id, category='notifications'):
        url = f"{self.website_api_url}/api/sol/{category}/{semester}/{item_id}"
        headers = {"x-scraper-key": self.scraper_key}
        resp = self._request_with_retry("DELETE", url, headers=headers)
        if resp is not None and resp.status_code in [200, 204]:
            return True
        else:
            print(f"  [API]: DELETE {url} FAILED (Status: {resp.status_code if resp else 'No Response'})")
            if resp: print(f"  [API]: Response: {resp.text[:200]}")
            return False

    def get_from_website(self, semester, category='notifications'):
        url = f"{self.website_api_url}/api/sol/{category}/{semester}"
        resp = self._request_with_retry("GET", url)
        if resp and resp.status_code == 200:
            try:
                data = resp.json().get('data')
                return data if isinstance(data, list) else []
            except Exception:
                return []
        return []

    def clear_category(self, category):
        """Atomic Hard Reset: Clears an entire category on the backend"""
        url = f"{self.website_api_url}/api/sol/{category}/clear-all"
        headers = {"x-scraper-key": self.scraper_key, "Content-Type": "application/json"}
        resp = self._request_with_retry("POST", url, headers=headers)
        if resp and resp.status_code == 200:
            print(f"[RESET]: Successfully cleared category '{category}' on backend.")
            return True
        else:
            print(f"[RESET]: Failed to clear category '{category}' (Status: {resp.status_code if resp else 'No Response'})")
            return False

    def sync_bulk_to_website(self, category, semester, items):
        """
        🚀 BULK SYNC: Sends a full list of current notices for a semester.
        The backend handles Adds, Updates (links), and Deletions.
        """
        url = f"{self.website_api_url}/api/sol/sync-bulk/{category}/{semester}"
        payload = {"items": items}
        headers = {"Content-Type": "application/json", "x-scraper-key": self.scraper_key}
        
        print(f"[API][BULK]: Syncing {len(items)} items for {category} Semester {semester}...")
        resp = self._request_with_retry("POST", url, json=payload, headers=headers)
        
        if resp is not None:
            try:
                stats = resp.json().get('stats', {})
                print(f"  [API][BULK]: Success | Added: {stats.get('added',0)}, Updated: {stats.get('updated',0)}, Deleted: {stats.get('deleted',0)}")
                return stats # Return full stats
            except Exception:
                print(f"  [API][BULK]: Success (Status: {resp.status_code})")
                return {"success": True}
        else:
            print(f"  [API][BULK]: FAILED (No response)")
            return {"success": False, "error": "No Response"}

    def clear_blacklist(self):
        """Clears the backend's notification blacklist (sol_deleted_notifications)"""
        url = f"{self.website_api_url}/api/sol/debug/clear-blacklist"
        headers = {"x-scraper-key": self.scraper_key, "Content-Type": "application/json"}
        resp = self._request_with_retry("POST", url, headers=headers)
        if resp and resp.status_code == 200:
            print("[RESET]: Successfully cleared backend notification blacklist.")
            return True
        else:
            print(f"[RESET]: Failed to clear blacklist (Status: {resp.status_code if resp else 'No Response'})")
            return False
