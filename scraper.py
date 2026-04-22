# pyre-ignore-all-errors
# pyre-unsafe
# type: ignore
from __future__ import annotations
import asyncio
import datetime
import re
import random
import os
import json
import base64
import sys
import time
import argparse
import subprocess as _subprocess
from urllib.parse import urljoin
from typing import List, Dict, Any, Optional, Set
import asyncio.subprocess

# Robust local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ThreadPoolExecutor

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ImportError:
    pass

# ─────────────────────────────────────────────
# IMPORTS — All graceful fallbacks
# ─────────────────────────────────────────────
try:
    from playwright.async_api import async_playwright, Page, BrowserContext  # type: ignore
    from playwright_stealth import stealth_async  # type: ignore
except ImportError:
    pass

try:
    from patchright.async_api import async_playwright as patchright_playwright  # type: ignore
except (ImportError, OSError, Exception):
    patchright_playwright = None  # type: ignore

try:
    from notifier import Notifier  # type: ignore
except ImportError:
    pass

try:
    import requests # type: ignore
except ImportError:
    pass

try:
    from curl_cffi import requests as cffi_requests  # type: ignore
except (ImportError, OSError, Exception):
    cffi_requests = None  # type: ignore

try:
    from bs4 import BeautifulSoup  # type: ignore
except ImportError:
    pass

try:
    import dateutil.parser as dparser  # type: ignore
except ImportError:
    pass

try:
    import httpx  # type: ignore
except (ImportError, OSError, Exception):
    httpx = None  # type: ignore

try:
    import cloudscraper as cloudscraper_lib  # type: ignore
except (ImportError, OSError, Exception):
    cloudscraper_lib = None  # type: ignore

try:
    import tls_client as tls_client_lib  # type: ignore
except (ImportError, OSError, Exception):
    tls_client_lib = None  # type: ignore

try:
    import nodriver as uc_nodriver  # type: ignore
except (ImportError, OSError, Exception):
    uc_nodriver = None  # type: ignore

try:
    from camoufox.async_api import AsyncCamoufox  # type: ignore
except (ImportError, OSError, Exception):
    AsyncCamoufox = None  # type: ignore

try:
    from seleniumbase import Driver as SBDriver  # type: ignore
except (ImportError, OSError, Exception):
    SBDriver = None  # type: ignore

try:
    import undetected_chromedriver as uc_chrome  # type: ignore
except (ImportError, OSError, Exception):
    uc_chrome = None  # type: ignore

try:
    from DrissionPage import ChromiumPage, ChromiumOptions  # type: ignore
except (ImportError, OSError, Exception):
    ChromiumPage = Any
    ChromiumOptions = Any

try:
    from botasaurus.request import request as botasaurus_request, AntiDetectRequests  # type: ignore
except (ImportError, OSError, Exception):
    botasaurus_request = Any
    AntiDetectRequests = Any

try:
    from pydoll.browser.chrome import Chrome as PydollChrome  # type: ignore
except (ImportError, OSError, Exception):
    PydollChrome = Any

try:
    from scrapling import StealthyFetcher, PlayWrightFetcher  # type: ignore
except (ImportError, OSError, Exception):
    StealthyFetcher = Any
    PlayWrightFetcher = Any

try:
    import seleniumwire.undetected_chromedriver as swire_uc  # type: ignore
except (ImportError, OSError, Exception):
    swire_uc = Any

try:
    import pychrome as pychrome_lib  # type: ignore
except (ImportError, OSError, Exception):
    pychrome_lib = None  # type: ignore

try:
    from fp.fp import FreeProxy  # type: ignore
except (ImportError, OSError, Exception):
    FreeProxy = None  # type: ignore

try:
    import proxybroker as pb_lib  # type: ignore
except (ImportError, OSError, Exception):
    pb_lib = None  # type: ignore


# ─────────────────────────────────────────────
# HUMAN BOT — Full behavior simulation
# ─────────────────────────────────────────────
class HumanBot:
    def __init__(self, page: Any):
        self.page = page

    async def bezier_move(self, tx: int, ty: int):
        try:
            vp = self.page.viewport_size or {"width": 1366, "height": 768}
            sx, sy = random.randint(0, vp["width"]), random.randint(0, vp["height"])
            cp1x = sx + random.randint(-200, 200)
            cp1y = sy + random.randint(-200, 200)
            cp2x = tx + random.randint(-100, 100)
            cp2y = ty + random.randint(-100, 100)
            steps = random.randint(20, 40)
            for i in range(steps + 1):
                t = i / steps
                x = (1-t)**3*sx + 3*(1-t)**2*t*cp1x + 3*(1-t)*t**2*cp2x + t**3*tx
                y = (1-t)**3*sy + 3*(1-t)**2*t*cp1y + 3*(1-t)*t**2*cp2y + t**3*ty
                await self.page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.005, 0.015))
        except Exception:
            pass

    async def click(self, selector: str):
        try:
            el = self.page.locator(selector).first
            box = await el.bounding_box()
            if box:
                tx = box["x"] + box["width"] * random.uniform(0.3, 0.7)
                ty = box["y"] + box["height"] * random.uniform(0.3, 0.7)
                await self.bezier_move(int(tx), int(ty))
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await self.page.mouse.down()
                await asyncio.sleep(random.uniform(0.05, 0.12))
                await self.page.mouse.up()
                await asyncio.sleep(random.uniform(0.3, 0.8))
        except Exception:
            try:
                await self.page.locator(selector).first.click()
            except Exception:
                pass

    async def scroll(self, amount: int = 500):
        steps = random.randint(3, 8)
        for _ in range(steps):
            await self.page.mouse.wheel(0, amount // steps + random.randint(-30, 30))
            await asyncio.sleep(random.uniform(0.08, 0.25))
            if random.random() < 0.1:
                await asyncio.sleep(random.uniform(0.5, 1.5))

    async def read(self, duration: float = 5.0):
        end = time.time() + duration
        while time.time() < end:
            action = random.choices(["scroll", "move", "pause"], weights=[0.4, 0.3, 0.3])[0]
            if action == "scroll":
                await self.scroll(random.randint(100, 400))
            elif action == "move":
                vp = self.page.viewport_size or {"width": 1366, "height": 768}
                await self.bezier_move(
                    random.randint(50, vp["width"] - 50),
                    random.randint(50, vp["height"] - 50)
                )
            else:
                await asyncio.sleep(random.uniform(0.5, 2.0))

    async def random_type(self, text: str):
        """Human-like typing with variable speed and occasional typos"""
        for char in text:
            if random.random() < 0.04:
                wrong = random.choice("abcdefghijklmnopqrstuvwxyz")
                await self.page.keyboard.type(wrong)
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await self.page.keyboard.press("Backspace")
                await asyncio.sleep(random.uniform(0.05, 0.15))
            await self.page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.04, 0.22))
            if random.random() < 0.05:
                await asyncio.sleep(random.uniform(0.3, 1.2))

    async def tab_switch_simulation(self):
        """Simulate tab switching (visibilitychange event)"""
        try:
            await self.page.evaluate("""() => {
                Object.defineProperty(document, 'hidden', { get: () => true, configurable: true });
                document.dispatchEvent(new Event('visibilitychange'));
            }""")
            await asyncio.sleep(random.uniform(1.5, 4.0))
            await self.page.evaluate("""() => {
                Object.defineProperty(document, 'hidden', { get: () => false, configurable: true });
                document.dispatchEvent(new Event('visibilitychange'));
                window.dispatchEvent(new Event('focus'));
            }""")
            await asyncio.sleep(random.uniform(0.5, 1.5))
        except Exception:
            pass

    async def back_button_behavior(self):
        """Simulate browser back + forward"""
        try:
            await self.page.go_back(wait_until="domcontentloaded", timeout=10000)
            await asyncio.sleep(random.uniform(1.0, 2.5))
            await self.page.go_forward(wait_until="domcontentloaded", timeout=10000)
            await asyncio.sleep(random.uniform(1.0, 2.0))
        except Exception:
            pass

    async def copy_paste_simulation(self):
        """Simulate Ctrl+A, Ctrl+C"""
        try:
            vp = self.page.viewport_size or {"width": 1366, "height": 768}
            await self.page.mouse.click(
                random.randint(100, vp["width"] - 100),
                random.randint(200, vp["height"] - 100)
            )
            await asyncio.sleep(random.uniform(0.2, 0.5))
            if random.random() < 0.5:
                await self.page.keyboard.down("Control")
                await self.page.keyboard.press("a")
                await self.page.keyboard.up("Control")
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await self.page.keyboard.down("Control")
                await self.page.keyboard.press("c")
                await self.page.keyboard.up("Control")
            await asyncio.sleep(random.uniform(0.3, 0.8))
        except Exception:
            pass

    async def right_click_simulation(self):
        """Simulate right-click + Escape"""
        try:
            vp = self.page.viewport_size or {"width": 1366, "height": 768}
            tx = random.randint(200, vp["width"] - 200)
            ty = random.randint(200, vp["height"] - 200)
            await self.bezier_move(tx, ty)
            await asyncio.sleep(random.uniform(0.1, 0.3))
            await self.page.mouse.click(tx, ty, button="right")
            await asyncio.sleep(random.uniform(0.5, 1.5))
            await self.page.keyboard.press("Escape")
            await asyncio.sleep(random.uniform(0.2, 0.5))
        except Exception:
            pass

    async def full_human_session(self, duration: float = 10.0):
        """Mix all behaviors for realistic session"""
        end = time.time() + duration
        behaviors = [
            (self.scroll, 0.35),
            (self.read, 0.25),
            (self.tab_switch_simulation, 0.1),
            (self.right_click_simulation, 0.1),
            (self.copy_paste_simulation, 0.1),
        ]
        fns = [b[0] for b in behaviors]
        wts = [b[1] for b in behaviors]
        while time.time() < end:
            fn = random.choices(fns, weights=wts)[0]
            try:
                if fn == self.scroll:
                    await self.scroll(random.randint(100, 500))
                elif fn == self.read:
                    await self.read(random.uniform(1, 3))
                else:
                    await fn() # type: ignore
            except Exception:
                pass
            await asyncio.sleep(random.uniform(0.3, 1.5))

    @staticmethod
    def js_mask_script() -> str:
        return """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = { runtime: {}, loadTimes: () => {}, csi: () => {}, app: {} };
        Object.defineProperty(navigator, 'languages', { get: () => ['en-IN', 'en-US', 'en', 'hi'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
        Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
        Object.defineProperty(navigator, 'connection', {
            get: () => ({ effectiveType: '4g', rtt: 50, downlink: 10, saveData: false })
        });
        const getParam = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(p) {
            if (p === 37445) return 'NVIDIA Corporation';
            if (p === 37446) return 'NVIDIA GeForce RTX 3080';
            return getParam.apply(this, arguments);
        };
        const origCtx = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function(type) {
            const ctx = origCtx.apply(this, arguments);
            if (type === '2d' && ctx) {
                const orig = ctx.getImageData;
                ctx.getImageData = function() {
                    const img = orig.apply(this, arguments);
                    img.data[0] = img.data[0] ^ 1;
                    return img;
                };
            }
            return ctx;
        };
        if (navigator.getBattery) {
            navigator.getBattery = () => Promise.resolve({
                charging: true, chargingTime: 0, dischargingTime: Infinity, level: 0.89,
                addEventListener: () => {}, removeEventListener: () => {}
            });
        }
        Object.defineProperty(screen, 'width', { get: () => 1366 });
        Object.defineProperty(screen, 'height', { get: () => 768 });
        Object.defineProperty(document, 'hidden', { get: () => false });
        Object.defineProperty(document, 'visibilityState', { get: () => 'visible' });
        const origPerms = window.navigator.permissions.query;
        window.navigator.permissions.query = (p) => p.name === 'notifications'
            ? Promise.resolve({ state: Notification.permission })
            : origPerms(p);
        """


# ─────────────────────────────────────────────
# MAIN SCRAPER CLASS — v100.0 OMNI-CRAWLER
# ─────────────────────────────────────────────
class MBAScraper:
    def __init__(self, target_mode: str = "all", force_sync: bool = False):
        self.target_mode = target_mode
        self.force_sync = force_sync
        self.base_url = "https://sol.du.ac.in"
        self.keywords = ['MBA', 'Master of Business Administration']
        self.visited = set()
        self.notices = []
        self.discovery_queue = [
            "https://sol.du.ac.in/home.php",
            "https://web.sol.du.ac.in/home",
            "https://sol.du.ac.in/all-notices.php",
            "https://web.sol.du.ac.in/info/online-class-schedule",
            "https://web.sol.du.ac.in/info/all-pg-class-time-table-sem-3-and-5"
        ]
        self.class_schedule_url = "https://web.sol.du.ac.in/my/team_schedules/vcs.php"
        self.parent_url = "https://web.sol.du.ac.in/info/online-class-schedule"
        self.current_url = ""
        self.current_year = datetime.datetime.now().year

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        ]
        self.mobile_agents = [
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
        ]
        self.user_agent = random.choice(self.user_agents)

        self.keys = {
            "SCRAPER_API": os.environ.get("SCRAPER_API_KEY") or os.environ.get("SCRAPERAPI_KEY", ""),
            "WSAI": os.environ.get("WEBSCRAPING_AI_KEY", ""),
            "ANT": os.environ.get("SCRAPER_ANT_KEY", ""),
            "CF_WORKER": os.environ.get("CF_WORKER_URL", ""),
            "TOR": os.environ.get("TOR_PROXY", ""),
            "SOL_COOKIES": os.environ.get("SOL_COOKIES", ""),
            "NETLIFY": os.environ.get("NETLIFY_PROXY_URL", ""),
            "VERCEL": os.environ.get("VERCEL_PROXY_URL", ""),
            "I2P": os.environ.get("I2P_PROXY", ""),
        }
        for k, v in self.keys.items():
            if v:
                print(f"[OMNI][KEY]: {k} ✅ present")
        
        # v73.9: Manual Deletion Persistence
        self.dismissed_file = "dismissed_links.json"
        self.dismissed_links = self._load_json(self.dismissed_file, set)
        
        # v100.2: Persistent Discovery Dates (Solves shifting dates issue)
        self.discovery_file = "discovery_dates.json"
        self.discovery_dates = self._load_json(self.discovery_file, dict)
        
        # v100.1: Hard Blacklist for unwanted topics (e.g., Library Notifications)
        self.blacklist_keywords = ['library', 'ai in libraries', 'books', 'librarian']
        self.blacklist_links = ['library_3.html', '/library_']
        
        print(f"[OMNI]: Loaded {len(self.dismissed_links)} dismissed links and {len(self.discovery_dates)} discovery dates.")

    def _load_json(self, path: str, type_fn: Any = list) -> Any:
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return type_fn(data)
        except Exception:
            pass
        return type_fn()

    def _save_json(self, path: str, data: Any):
        try:
            with open(path, "w", encoding="utf-8") as f:
                # Convert set to list if needed
                if isinstance(data, set):
                    data = list(data)
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[FILE-ERROR]: Could not save {path} -> {e}")

    def _iframe_headers(self, ua: Optional[str] = None) -> dict:
        return {
            "User-Agent": ua or self.user_agent,
            "Referer": self.parent_url,
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="124", "Google Chrome";v="124"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
            "upgrade-insecure-requests": "1",
        }

    # ═══════════════════════════════════════════
    # M01: curl_cffi — TLS fingerprint rotation
    # ═══════════════════════════════════════════
    async def m01_cffi(self, url: str) -> Optional[str]:
        if cffi_requests is None:
            print("[M01][CFFI]: curl_cffi not installed. Skipping.")
            return None
        print("[M01][CFFI]: TLS fingerprint rotation...")
        for fp in ["chrome124", "chrome120", "chrome116", "firefox122", "edge101"]:
            try:
                session = cffi_requests.Session(impersonate=fp) # type: ignore
                session.get("https://sol.du.ac.in/home.php", timeout=12)
                time.sleep(1)
                session.get("https://web.sol.du.ac.in/home", timeout=12)
                time.sleep(1)
                h = self._iframe_headers() if "vcs.php" in url else {"User-Agent": self.user_agent}
                r = session.get(url, headers=h, timeout=30)
                print(f"[M01][CFFI][{fp}]: {r.status_code}")
                if r.status_code == 200:
                    return r.text
            except Exception as e:
                print(f"[M01][CFFI][{fp}]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M02: tls-client — JA3/JA4 rotation
    # ═══════════════════════════════════════════
    async def m02_tls_client(self, url: str) -> Optional[str]:
        if tls_client_lib is None:
            print("[M02][TLS-CLIENT]: tls-client not installed. Skipping.")
            return None
        print("[M02][TLS-CLIENT]: JA3/JA4 fingerprint...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                for profile in ["chrome_120", "chrome_117", "firefox_120", "safari_16_0"]:
                    try:
                        session = tls_client_lib.Session( # type: ignore
                            client_identifier=profile,
                            random_tls_extension_order=True
                        )
                        session.get("https://sol.du.ac.in/home.php", timeout_seconds=12)
                        time.sleep(1)
                        r = session.get(url, headers=self._iframe_headers(), timeout_seconds=30)
                        print(f"[M02][TLS-CLIENT][{profile}]: {r.status_code}")
                        if r.status_code == 200:
                            return r.text
                    except Exception as e:
                        print(f"[M02][TLS-CLIENT][{profile}]: {e}")
                return None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M02][TLS-CLIENT]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M03: httpx HTTP/2
    # ═══════════════════════════════════════════
    async def m03_httpx(self, url: str) -> Optional[str]:
        if httpx is None:
            print("[M03][HTTPX-H2]: httpx not installed. Skipping.")
            return None
        print("[M03][HTTPX-H2]: HTTP/2 fingerprint...")
        try:
            async with httpx.AsyncClient(http2=True, follow_redirects=True, timeout=30) as client:
                await client.get("https://sol.du.ac.in/home.php",
                                 headers={"User-Agent": self.user_agent})
                await asyncio.sleep(1)
                r = await client.get(url, headers=self._iframe_headers())
                print(f"[M03][HTTPX-H2]: {r.status_code}")
                if r.status_code == 200:
                    return r.text
        except Exception as e:
            print(f"[M03][HTTPX-H2]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M04: cloudscraper
    # ═══════════════════════════════════════════
    async def m04_cloudscraper(self, url: str) -> Optional[str]:
        if cloudscraper_lib is None:
            print("[M04][CLOUDSCRAPER]: cloudscraper not installed. Skipping.")
            return None
        print("[M04][CLOUDSCRAPER]: JS challenge bypass...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                scraper = cloudscraper_lib.create_scraper( # type: ignore
                    browser={"browser": "chrome", "platform": "windows", "mobile": False}
                )
                scraper.get("https://sol.du.ac.in/home.php", timeout=12)
                time.sleep(1)
                r = scraper.get(url, headers=self._iframe_headers(), timeout=30)
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M04][CLOUDSCRAPER]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M05: Manual cookies (SOL_COOKIES env)
    # ═══════════════════════════════════════════
    async def m05_manual_cookies(self, url: str) -> Optional[str]:
        if cffi_requests is None:
            print("[M05][COOKIES]: curl_cffi not installed. Skipping.")
            return None
        cookie_str = self.keys["SOL_COOKIES"]
        if not cookie_str:
            return None
        print("[M05][COOKIES]: Injected session cookies...")
        try:
            session = cffi_requests.Session(impersonate="chrome124") # type: ignore
            h = self._iframe_headers()
            h["Cookie"] = cookie_str
            r = session.get(url, headers=h, timeout=30)
            print(f"[M05][COOKIES]: {r.status_code}")
            return r.text if r.status_code == 200 else None
        except Exception as e:
            print(f"[M05][COOKIES]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M06: Wayback Machine
    # ═══════════════════════════════════════════
    async def m06_wayback(self, url: str) -> Optional[str]:
        print("[M06][WAYBACK]: archive.org snapshot...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(
                    f"http://archive.org/wayback/available?url={url}", timeout=10
                ).json()
                snap = r.get("archived_snapshots", {}).get("closest", {}).get("url")
                if snap:
                    return requests.get(snap, timeout=20).text
                return None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M06][WAYBACK]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M07: Wayback CDX Index
    # ═══════════════════════════════════════════
    async def m07_cdx(self, url: str) -> Optional[str]:
        print("[M07][CDX]: Wayback CDX historical index...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                api = "http://web.archive.org/cdx/search/cdx?url=sol.du.ac.in&matchType=domain&filter=mimetype:application/pdf&limit=30&output=json"
                data = requests.get(api, timeout=12).json()
                if data and len(data) > 1:
                    html = "<html><body>"
                    for e in data[1:]:
                        html += f'<a href="{e[2]}">{e[2]}</a> '
                    return html + "</body></html>"
                return None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M07][CDX]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M08: Google Cache
    # ═══════════════════════════════════════════
    async def m08_google_cache(self, url: str) -> Optional[str]:
        print("[M08][GCACHE]: Google Cache...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(
                    f"http://webcache.googleusercontent.com/search?q=cache:{url}",
                    headers={"User-Agent": self.user_agent}, timeout=12
                )
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M08][GCACHE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M09: Bing Cache
    # ═══════════════════════════════════════════
    async def m09_bing_cache(self, url: str) -> Optional[str]:
        print("[M09][BING-CACHE]: Bing Cache...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(
                    f"https://cc.bingj.com/cache.aspx?q={url}&url={url}",
                    headers={"User-Agent": self.user_agent}, timeout=12
                )
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M09][BING-CACHE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M10: Yandex Cache
    # ═══════════════════════════════════════════
    async def m10_yandex_cache(self, url: str) -> Optional[str]:
        print("[M10][YANDEX-CACHE]: Yandex Cache...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(
                    f"https://yandex.com/search/?text=cache:{url}",
                    headers={"User-Agent": self.user_agent}, timeout=12
                )
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M10][YANDEX-CACHE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M11: CommonCrawl
    # ═══════════════════════════════════════════
    async def m11_commoncrawl(self, url: str) -> Optional[str]:
        print("[M11][COMMONCRAWL]: CommonCrawl index...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                import gzip
                api = f"http://index.commoncrawl.org/CC-MAIN-2024-10-index?url={url}&output=json"
                r = requests.get(api, timeout=12)
                if r.status_code == 200:
                    lines = r.text.strip().split("\n")
                    if lines:
                        entry = json.loads(lines[0])
                        filename = entry.get("filename")
                        offset = int(entry.get("offset", 0))
                        length = int(entry.get("length", 0))
                        if filename:
                            s3url = f"https://data.commoncrawl.org/{filename}"
                            resp = requests.get(
                                s3url,
                                headers={"Range": f"bytes={offset}-{offset+length-1}"},
                                timeout=20
                            )
                            try:
                                content = gzip.decompress(resp.content).decode("utf-8", errors="ignore")
                                idx = content.lower().find("<html")
                                return content[idx:] if idx >= 0 else None # type: ignore
                            except Exception:
                                pass
                return None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M11][COMMONCRAWL]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M12: CachedView.nl
    # ═══════════════════════════════════════════
    async def m12_cachedview(self, url: str) -> Optional[str]:
        print("[M12][CACHEDVIEW]: CachedView.nl...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(
                    f"https://cachedview.nl/cachedPage.php?url={url}",
                    headers={"User-Agent": self.user_agent}, timeout=12
                )
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M12][CACHEDVIEW]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M13: Cloudflare Worker proxy
    # ═══════════════════════════════════════════
    async def m13_cf_worker(self, url: str) -> Optional[str]:
        if not self.keys["CF_WORKER"]:
            return None
        print("[M13][CF-WORKER]: Cloudflare Worker proxy...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(self.keys["CF_WORKER"], params={"url": url}, timeout=40)
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M13][CF-WORKER]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M14: Vercel Edge proxy
    # ═══════════════════════════════════════════
    async def m14_vercel(self, url: str) -> Optional[str]:
        if not self.keys["VERCEL"]:
            return None
        print("[M14][VERCEL]: Vercel Edge proxy...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(self.keys["VERCEL"], params={"url": url}, timeout=40)
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M14][VERCEL]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M15: Netlify Functions proxy
    # ═══════════════════════════════════════════
    async def m15_netlify(self, url: str) -> Optional[str]:
        if not self.keys["NETLIFY"]:
            return None
        print("[M15][NETLIFY]: Netlify proxy...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                r = requests.get(self.keys["NETLIFY"], params={"url": url}, timeout=40)
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M15][NETLIFY]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M16: Tor proxy
    # ═══════════════════════════════════════════
    async def m16_tor(self, url: str) -> Optional[str]:
        if not self.keys["TOR"]:
            return None
        print(f"[M16][TOR]: Tor proxy {self.keys['TOR']}...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                proxies = {"http": self.keys["TOR"], "https": self.keys["TOR"]}
                s = requests.Session() # type: ignore
                s.get("https://sol.du.ac.in/home.php", proxies=proxies, timeout=25)
                r = s.get(url, headers=self._iframe_headers(), proxies=proxies, timeout=40)
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M16][TOR]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M17: I2P outproxy
    # ═══════════════════════════════════════════
    async def m17_i2p(self, url: str) -> Optional[str]:
        i2p = self.keys.get("I2P", "http://127.0.0.1:4444")
        print(f"[M17][I2P]: I2P outproxy...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                proxies = {"http": i2p, "https": i2p}
                r = requests.get(url, headers=self._iframe_headers(), proxies=proxies, timeout=50)
                return r.text if r.status_code == 200 else None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M17][I2P]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M18: FreeProxy rotation
    # ═══════════════════════════════════════════
    async def m18_freeproxy(self, url: str) -> Optional[str]:
        if FreeProxy is None:
            print("[M18][FREEPROXY]: fp-proxy not installed. Skipping.")
            return None
        print("[M18][FREEPROXY]: Free proxy rotation...")
        try:
            loop = asyncio.get_event_loop()
            fp_tool = FreeProxy # Local reference for IDE type stability
            if not fp_tool: return None

            def _run():
                for _ in range(5):
                    try:
                        proxy_addr = fp_tool(rand=True, timeout=3).get()
                        if not proxy_addr:
                            continue
                        proxies = {"http": proxy_addr, "https": proxy_addr}
                        s = requests.Session() # type: ignore
                        s.get("https://sol.du.ac.in/home.php",
                              proxies=proxies, timeout=12,
                              headers={"User-Agent": self.user_agent})
                        r = s.get(url, headers=self._iframe_headers(),
                                  proxies=proxies, timeout=20)
                        if r.status_code == 200:
                            return r.text
                    except Exception:
                        continue
                return None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M18][FREEPROXY]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M19: IPv6 rotation
    # ═══════════════════════════════════════════
    async def m19_ipv6(self, url: str) -> Optional[str]:
        print("[M19][IPv6]: IPv6 address rotation...")
        try:
            import socket
            loop = asyncio.get_event_loop()
            def _run():
                orig = socket.getaddrinfo
                def ipv6_only(host, port, family=0, type=0, proto=0, flags=0):
                    return orig(host, port, socket.AF_INET6, type, proto, flags)
                socket.getaddrinfo = ipv6_only
                try:
                    session = cffi_requests.Session(impersonate="chrome124") # type: ignore
                    session.get("https://sol.du.ac.in/home.php", timeout=12)
                    r = session.get(url, headers=self._iframe_headers(), timeout=25)
                    return r.text if r.status_code == 200 else None
                finally:
                    socket.getaddrinfo = orig
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M19][IPv6]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M20: DNS-over-HTTPS
    # ═══════════════════════════════════════════
    async def m20_doh(self, url: str) -> Optional[str]:
        print("[M20][DoH]: DNS-over-HTTPS resolution...")
        try:
            loop = asyncio.get_event_loop()
            def _resolve():
                r = requests.get(
                    "https://cloudflare-dns.com/dns-query?name=web.sol.du.ac.in&type=A",
                    headers={"Accept": "application/dns-json"}, timeout=8
                )
                if r.status_code == 200:
                    ans = r.json().get("Answer", [])
                    return ans[0].get("data") if ans else None
                return None
            ip = await loop.run_in_executor(None, _resolve) # type: ignore
            if ip:
                def _run(resolved_ip):
                    import warnings
                    warnings.filterwarnings("ignore")
                    session = cffi_requests.Session(impersonate="chrome124") # type: ignore
                    h = {**self._iframe_headers(), "Host": "web.sol.du.ac.in"}
                    target = url.replace("web.sol.du.ac.in", resolved_ip)
                    r = session.get(target, headers=h, verify=False, timeout=25)
                    return r.text if r.status_code == 200 else None
                return await loop.run_in_executor(None, _run, ip)
        except Exception as e:
            print(f"[M20][DoH]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M21: Request timing jitter
    # ═══════════════════════════════════════════
    async def m21_timing_jitter(self, url: str) -> Optional[str]:
        print("[M21][TIMING-JITTER]: Human-paced timing with jitter...")
        try:
            session = cffi_requests.Session(impersonate="chrome124") # type: ignore
            loop = asyncio.get_event_loop()
            sequence = [
                ("https://sol.du.ac.in/home.php", random.uniform(2.5, 5.0)),
                ("https://web.sol.du.ac.in/home", random.uniform(3.0, 6.0)),
                ("https://web.sol.du.ac.in/info/student-support", random.uniform(2.0, 4.0)),
                (self.parent_url, random.uniform(4.0, 8.0)),
            ]
            for seq_url, wait in sequence:
                def _get(u):
                    return session.get(u, headers={"User-Agent": self.user_agent}, timeout=15)
                await loop.run_in_executor(None, _get, seq_url) # type: ignore
                if random.random() < 0.2:
                    await asyncio.sleep(random.uniform(8, 15))
                else:
                    await asyncio.sleep(wait)
            def _final():
                return session.get(url, headers=self._iframe_headers(), timeout=30)
            r = await loop.run_in_executor(None, _final) # pyre-ignore[6]
            print(f"[M21][TIMING-JITTER]: {r.status_code}")
            return r.text if r.status_code == 200 else None
        except Exception as e:
            print(f"[M21][TIMING-JITTER]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M22: curl-impersonate subprocess
    # ═══════════════════════════════════════════
    async def m22_curl_impersonate(self: Any, url: str) -> Optional[str]:
        print("[M22][CURL-IMPERSONATE]: Rust TLS via curl-impersonate binary...")
        try:
            for binary in ["curl-impersonate-chrome", "curl_chrome116", "curl"]:
                try:
                    cmd = [
                        binary, "--silent", "--location",
                        "-H", f"Referer: {self.parent_url}",
                        "-H", "sec-fetch-dest: iframe",
                        "-H", "sec-fetch-mode: navigate",
                        "-H", f"User-Agent: {self.user_agent}",
                        "--max-time", "30", url
                    ]
                    proc = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=40)
                    html = stdout.decode("utf-8", errors="ignore")
                    if html and self._is_valid(html): # type: ignore
                        return html
                except FileNotFoundError:
                    continue
        except Exception as e:
            print(f"[M22][CURL-IMPERSONATE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M23: ScraperAPI
    # ═══════════════════════════════════════════
    async def m23_scraperapi(self, url: str) -> Optional[str]:
        if not self.keys["SCRAPER_API"]:
            return None
        print("[M23][SCRAPERAPI]: ScraperAPI residential proxy...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                api = f"http://api.scraperapi.com?api_key={self.keys['SCRAPER_API']}&url={url}&render_js=true"
                return requests.get(api, timeout=60).text
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M23][SCRAPERAPI]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M24: ScraperAnt (10k free/mo)
    # ═══════════════════════════════════════════
    async def m24_scraperант(self, url: str) -> Optional[str]:
        if not self.keys["ANT"]:
            return None
        print("[M24][SCRAPERАNT]: ScraperAnt API...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                api = f"https://api.scraperant.com/v2/general?url={url}&x-api-key={self.keys['ANT']}&browser=true"
                return requests.get(api, timeout=60).text
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M24][SCRAPERАNT]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M25: WebScraping.ai (1k free/mo)
    # ═══════════════════════════════════════════
    async def m25_wsai(self, url: str) -> Optional[str]:
        if not self.keys["WSAI"]:
            return None
        print("[M25][WSAI]: WebScraping.ai...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                api = f"https://api.webscraping.ai/html?url={url}&api_key={self.keys['WSAI']}&proxy=residential&render=true"
                return requests.get(api, timeout=60).text
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M25][WSAI]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M26: Playwright Ghost Fetch
    # ═══════════════════════════════════════════
    async def m26_pw_ghost(self, url: str, context: Any) -> Optional[str]:
        print("[M26][PW-GHOST]: Playwright context iframe ghost fetch...")
        try:
            page = await context.new_page()
            await context.add_init_script(HumanBot.js_mask_script())
            bot = HumanBot(page)
            await page.goto(self.parent_url, wait_until="networkidle", timeout=60000)
            await bot.read(random.uniform(4, 7))
            response = await context.request.get(url, headers={
                "referer": self.parent_url,
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
            })
            await page.close()
            print(f"[M26][PW-GHOST]: {response.status}")
            if response.ok:
                return await response.text()
        except Exception as e:
            print(f"[M26][PW-GHOST]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M27: Playwright Full Human Bot
    # ═══════════════════════════════════════════
    async def m27_pw_human(self, url: str, context: Any) -> Optional[str]:
        print("[M27][PW-HUMAN]: Full Playwright human bot...")
        try:
            page = await context.new_page()
            bot = HumanBot(page)
            await page.goto("https://sol.du.ac.in/home.php",
                            wait_until="domcontentloaded", timeout=60000)
            await bot.read(random.uniform(3, 5))
            await page.goto("https://web.sol.du.ac.in/home",
                            wait_until="domcontentloaded", timeout=60000)
            await bot.read(random.uniform(3, 5))
            try:
                await bot.click("text='Student Support'")
                await asyncio.sleep(random.uniform(2, 4))
            except Exception:
                await page.goto("https://web.sol.du.ac.in/info/student-support",
                                wait_until="domcontentloaded", timeout=60000)
            await bot.read(random.uniform(2, 4))
            link_sel = "a:has-text('Online Class Schedule')"
            try:
                await page.wait_for_selector(link_sel, timeout=12000)
                async with context.expect_page(timeout=25000) as new_pg:
                    await bot.click(link_sel)
                target_page = await new_pg.value
            except Exception:
                await page.goto(self.parent_url, wait_until="networkidle", timeout=60000)
                target_page = page
            await target_page.wait_for_load_state("networkidle", timeout=60000)
            target_bot = HumanBot(target_page)
            await target_bot.full_human_session(duration=random.uniform(10, 15))
            # Try ghost fetch from new page's context
            try:
                response = await context.request.get(url, headers={
                    "referer": self.parent_url,
                    "sec-fetch-dest": "iframe",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                })
                print(f"[M27][PW-HUMAN][GHOST]: {response.status}")
                if response.ok:
                    html = await response.text()
                    await page.close()
                    try:
                        await target_page.close()
                    except Exception:
                        pass
                    return html
            except Exception:
                pass
            # Fallback: extract from frames
            html = await self._extract_frames_html(target_page)
            await page.close()
            try:
                await target_page.close()
            except Exception:
                pass
            return html
        except Exception as e:
            print(f"[M27][PW-HUMAN]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M28: Patchright
    # ═══════════════════════════════════════════
    async def m28_patchright(self, url: str) -> Optional[str]:
        if patchright_playwright is None:
            print("[M28][PATCHRIGHT]: patchright not installed. Skipping.")
            return None
        print("[M28][PATCHRIGHT]: Source-level CDP patch...")
        try:
            async with patchright_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
                )
                context = await browser.new_context(
                    user_agent=self.user_agent,
                    viewport={"width": 1366, "height": 768},
                    locale="en-IN", timezone_id="Asia/Kolkata"
                )
                await context.add_init_script(HumanBot.js_mask_script())
                page = await context.new_page()
                bot = HumanBot(page)
                await page.goto("https://sol.du.ac.in/home.php",
                                wait_until="domcontentloaded", timeout=60000)
                await bot.read(3)
                await page.goto(self.parent_url, wait_until="networkidle", timeout=60000)
                await bot.full_human_session(random.uniform(5, 8))
                response = await context.request.get(url, headers={
                    "referer": self.parent_url,
                    "sec-fetch-dest": "iframe",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                })
                await browser.close()
                print(f"[M28][PATCHRIGHT]: {response.status}")
                if response.ok:
                    return await response.text()
        except Exception as e:
            print(f"[M28][PATCHRIGHT]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M29: Nodriver
    # ═══════════════════════════════════════════
    async def m29_nodriver(self: Any, url: str) -> Optional[str]:
        if uc_nodriver is None:
            print("[M29][NODRIVER]: nodriver not installed. Skipping.")
            return None
        print("[M29][NODRIVER]: Direct CDP, no WebDriver...")
        try:
            browser = await uc_nodriver.start( # type: ignore
                headless=True,
                browser_args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = await browser.get("https://sol.du.ac.in/home.php")
            await asyncio.sleep(random.uniform(3, 5))
            page = await browser.get(self.parent_url)
            await asyncio.sleep(random.uniform(8, 12))
            html = await page.get_content()
            print(f"[M29][NODRIVER]: Got {len(html)} bytes")
            await browser.stop()
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M29][NODRIVER]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M30: Camoufox (Firefox C++)
    # ═══════════════════════════════════════════
    async def m30_camoufox(self, url: str) -> Optional[str]:
        if AsyncCamoufox is None:
            print("[M30][CAMOUFOX]: camoufox not installed. Skipping.")
            return None
        print("[M30][CAMOUFOX]: Firefox C++ fingerprint...")
        try:
            async with AsyncCamoufox(headless=True, geoip=True) as browser:
                page = await browser.new_page()
                await page.goto("https://sol.du.ac.in/home.php",
                                wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(random.uniform(3, 5))
                await page.goto(self.parent_url, wait_until="networkidle", timeout=60000)
                await asyncio.sleep(random.uniform(5, 8))
                try:
                    response = await page.context.request.get(url, headers={
                        "referer": self.parent_url,
                        "sec-fetch-dest": "iframe",
                        "sec-fetch-mode": "navigate",
                        "sec-fetch-site": "same-origin",
                    })
                    print(f"[M30][CAMOUFOX]: {response.status}")
                    if response.ok:
                        return await response.text()
                except Exception:
                    pass
                return await self._extract_frames_html(page)
        except Exception as e:
            print(f"[M30][CAMOUFOX]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M31: SeleniumBase UC Mode
    # ═══════════════════════════════════════════
    async def m31_seleniumbase(self: Any, url: str) -> Optional[str]: # pyre-ignore[10]
        if SBDriver is None:
            print("[M31][SELENIUMBASE-UC]: seleniumbase not installed. Skipping.")
            return None
        print("[M31][SELENIUMBASE-UC]: 89% AWS WAF bypass rate...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                driver = SBDriver(uc=True, headless=True, no_sandbox=True) # type: ignore
                try:
                    driver.uc_open_with_reconnect("https://sol.du.ac.in/home.php", reconnect_time=3)
                    time.sleep(random.uniform(2, 4))
                    driver.uc_open_with_reconnect(self.parent_url, reconnect_time=4)
                    time.sleep(random.uniform(6, 10))
                    return driver.get_page_source()
                finally:
                    driver.quit()
            html = await loop.run_in_executor(None, _run) # type: ignore
            print(f"[M31][SELENIUMBASE-UC]: {len(html) if html else 0} bytes")
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M31][SELENIUMBASE-UC]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M32: undetected-chromedriver
    # ═══════════════════════════════════════════
    async def m32_ucd(self: Any, url: str) -> Optional[str]:
        if uc_chrome is None:
            print("[M32][UCD]: undetected-chromedriver not installed. Skipping.")
            return None
        print("[M32][UCD]: undetected-chromedriver...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                opts = uc_chrome.ChromeOptions() # type: ignore
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                driver = uc_chrome.Chrome(options=opts, headless=True) # type: ignore
                try:
                    driver.get("https://sol.du.ac.in/home.php")
                    time.sleep(random.uniform(2, 4))
                    driver.get(self.parent_url)
                    time.sleep(random.uniform(6, 10))
                    return driver.page_source
                finally:
                    driver.quit()
            html = await loop.run_in_executor(None, _run) # type: ignore
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M32][UCD]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M33: DrissionPage
    # ═══════════════════════════════════════════
    async def m33_drissionpage(self: Any, url: str) -> Optional[str]:
        if ChromiumPage is None:
            print("[M33][DRISSIONPAGE]: DrissionPage not installed. Skipping.")
            return None
        print("[M33][DRISSIONPAGE]: Hybrid requests+browser...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                opts = ChromiumOptions() # pyre-ignore[29]
                opts.headless(True) # type: ignore
                opts.set_argument("--no-sandbox")
                opts.set_argument("--disable-dev-shm-usage")
                page = ChromiumPage(opts) # pyre-ignore[29]
                try:
                    page.get("https://sol.du.ac.in/home.php")
                    time.sleep(random.uniform(2, 4))
                    page.get(self.parent_url)
                    time.sleep(random.uniform(6, 10))
                    return page.html
                finally:
                    page.quit()
            html = await loop.run_in_executor(None, _run) # type: ignore
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M33][DRISSIONPAGE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M34: Pydoll (CDP direct)
    # ═══════════════════════════════════════════
    async def m34_pydoll(self, url: str) -> Optional[str]:
        if PydollChrome is None:
            print("[M34][PYDOLL]: pydoll not installed. Skipping.")
            return None
        print("[M34][PYDOLL]: CDP direct, no WebDriver artifacts...")
        try:
            async with PydollChrome(options={ # pyre-ignore[29]
                "args": ["--no-sandbox", "--disable-dev-shm-usage"],
                "headless": True
            }) as browser:
                tab = await browser.start()
                await tab.go_to("https://sol.du.ac.in/home.php")
                await asyncio.sleep(random.uniform(2, 4))
                await tab.go_to(self.parent_url)
                await asyncio.sleep(random.uniform(6, 10))
                el = await tab.get_element("html")
                html = str(el) if el else ""
                return html if html and self._is_valid(html) else None # pyre-ignore[7]
        except Exception as e:
            print(f"[M34][PYDOLL]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M35: Scrapling
    # ═══════════════════════════════════════════
    async def m35_scrapling(self: Any, url: str) -> Optional[str]:
        if StealthyFetcher is None:
            print("[M35][SCRAPLING]: scrapling not installed. Skipping.")
            return None
        print("[M35][SCRAPLING]: Adaptive stealth fetcher...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                for FetcherClass in [StealthyFetcher, PlayWrightFetcher]:
                    try:
                        fetcher = FetcherClass() # pyre-ignore[29]
                        resp = fetcher.fetch(self.parent_url) # type: ignore
                        if resp and resp.status == 200:
                            return resp.content
                    except Exception:
                        continue
                return None
            html = await loop.run_in_executor(None, _run) # type: ignore
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M35][SCRAPLING]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M36: Botasaurus
    # ═══════════════════════════════════════════
    async def m36_botasaurus(self: Any, url: str) -> Optional[str]:
        if botasaurus_request is None:
            print("[M36][BOTASAURUS]: botasaurus not installed. Skipping.")
            return None
        print("[M36][BOTASAURUS]: Human mouse + Google referer trick...")
        try:
            loop = asyncio.get_event_loop()
            parent = self.parent_url
            def _run():
                @botasaurus_request # type: ignore
                def fetch(request: AntiDetectRequests, data):
                    return request.get(parent, timeout=30).text # type: ignore
                results = fetch() # type: ignore
                return results[0] if results else None # type: ignore
            html = await loop.run_in_executor(None, _run) # type: ignore
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M36][BOTASAURUS]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M37: Selenium Wire
    # ═══════════════════════════════════════════
    async def m37_selenium_wire(self: Any, url: str) -> Optional[str]:
        if swire_uc is None:
            print("[M37][SELENIUM-WIRE]: selenium-wire not installed. Skipping.")
            return None
        print("[M37][SELENIUM-WIRE]: Request interception + replay...")
        try:
            loop = asyncio.get_event_loop()
            parent = self.parent_url
            def _run():
                opts = swire_uc.ChromeOptions() # type: ignore
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                driver = swire_uc.Chrome(options=opts, headless=True) # type: ignore
                try:
                    driver.get("https://sol.du.ac.in/home.php")
                    time.sleep(random.uniform(2, 4))
                    driver.get(parent)
                    time.sleep(random.uniform(6, 10))
                    # Try to capture vcs.php response from intercepted requests
                    for req in driver.requests: # pyre-ignore[16]
                        if "vcs.php" in req.url and req.response:
                            return req.response.body.decode("utf-8", errors="ignore")
                    return driver.page_source # pyre-ignore[16]
                finally:
                    driver.quit() # pyre-ignore[16]
            html = await loop.run_in_executor(None, _run) # type: ignore
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M37][SELENIUM-WIRE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M38: Puppeteer (Node.js subprocess)
    # ═══════════════════════════════════════════
    async def m38_puppeteer(self, url: str) -> Optional[str]:
        print("[M38][PUPPETEER]: Node.js Puppeteer subprocess...")
        try:
            parent = self.parent_url
            script = f"""
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
(async () => {{
    const browser = await puppeteer.launch({{
        headless: 'new',
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    }});
    const page = await browser.newPage();
    await page.setUserAgent('{self.user_agent}');
    await page.goto('https://sol.du.ac.in/home.php', {{waitUntil:'domcontentloaded'}});
    await new Promise(r => setTimeout(r, 3000));
    await page.goto('{parent}', {{waitUntil:'networkidle2', timeout:60000}});
    await new Promise(r => setTimeout(r, 8000));
    for (const frame of page.frames()) {{
        if (frame.url().includes('vcs')) {{
            const html = await frame.content();
            process.stdout.write('VCS:' + html);
            break;
        }}
    }}
    const html = await page.content();
    process.stdout.write('MAIN:' + html);
    await browser.close();
}})();
"""
            script_path = "/tmp/_puppeteer_sol.js"
            with open(script_path, "w") as f:
                f.write(script)
            proc = await asyncio.create_subprocess_exec( # type: ignore
                "node", script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=90)
            output = stdout.decode("utf-8", errors="ignore")
            if "VCS:" in output:
                html = output.split("VCS:")[1].split("MAIN:")[0]
                if html and self._is_valid(html): # type: ignore
                    return html
            if "MAIN:" in output:
                return output.split("MAIN:")[1]
        except Exception as e:
            print(f"[M38][PUPPETEER]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M39: pychrome raw CDP
    # ═══════════════════════════════════════════
    async def m39_pychrome(self, url: str) -> Optional[str]:
        if pychrome_lib is None:
            print("[M39][PYCHROME]: pychrome not installed. Skipping.")
            return None
        print("[M39][PYCHROME]: Raw CDP, no WebDriver...")
        try:
            loop = asyncio.get_event_loop()
            parent = self.parent_url
            ua = self.user_agent
            def _run():
                proc = _subprocess.Popen([
                    "google-chrome", "--headless", "--no-sandbox",
                    "--remote-debugging-port=9223",
                    "--disable-dev-shm-usage",
                    f"--user-agent={ua}"
                ], stdout=_subprocess.DEVNULL, stderr=_subprocess.DEVNULL)
                time.sleep(2)
                try:
                    browser = pychrome_lib.Browser(url="http://127.0.0.1:9223") # type: ignore
                    tab = browser.new_tab()
                    tab.start()
                    tab.Page.enable()
                    tab.Page.navigate(url="https://sol.du.ac.in/home.php")
                    time.sleep(3)
                    tab.Page.navigate(url=parent)
                    time.sleep(8)
                    result = tab.Runtime.evaluate(
                        expression="document.documentElement.outerHTML"
                    )
                    html = result.get("result", {}).get("value", "")
                    tab.stop()
                    browser.close_tab(tab)
                    return html
                finally:
                    proc.terminate()
            html = await loop.run_in_executor(None, _run) # type: ignore
            return str(html) if html and self._is_valid(html) else None # pyre-ignore[16,7]
        except Exception as e:
            print(f"[M39][PYCHROME]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M40: CSRF + Cookie harvest
    # ═══════════════════════════════════════════
    async def m40_csrf_cookies(self, url: str, context: Any) -> Optional[str]:
        print("[M40][CSRF-COOKIES]: Extract CSRF + cookies from live session...")
        try:
            page = await context.new_page()
            await page.goto(self.parent_url, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(3)
            csrf = await page.evaluate("""() => {
                const m = document.querySelector('meta[name="csrf-token"]');
                if (m) return m.getAttribute('content');
                const i = document.querySelector('input[name="_token"],input[name="csrf_token"]');
                return i ? i.value : null;
            }""")
            cookies = await context.cookies()
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            await page.close()
            if cookie_str:
                h = self._iframe_headers()
                h["Cookie"] = cookie_str
                if csrf:
                    h["X-CSRF-Token"] = csrf
                session = cffi_requests.Session(impersonate="chrome124") # type: ignore
                r = session.get(url, headers=h, timeout=30)
                print(f"[M40][CSRF-COOKIES]: {r.status_code}")
                if r.status_code == 200:
                    return r.text
        except Exception as e:
            print(f"[M40][CSRF-COOKIES]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M41: AWS ALB cookie forge
    # ═══════════════════════════════════════════
    async def m41_awsalb_forge(self, url: str) -> Optional[str]:
        print("[M41][AWSALB-FORGE]: Probing for AWSALB cookie on other pages...")
        try:
            loop = asyncio.get_event_loop()
            def _run():
                for probe in [
                    "https://web.sol.du.ac.in/home",
                    "https://web.sol.du.ac.in/info/student-support",
                    "https://web.sol.du.ac.in/info/about",
                ]:
                    try:
                        session = cffi_requests.Session(impersonate="chrome124") # type: ignore
                        session.get(probe, headers={"User-Agent": self.user_agent}, timeout=12)
                        if session.cookies.get("AWSALB"):
                            print(f"[M41][AWSALB-FORGE]: Got AWSALB from {probe}")
                            r = session.get(url, headers=self._iframe_headers(), timeout=25)
                            if r.status_code == 200:
                                return r.text
                    except Exception:
                        continue
                return None
            return await loop.run_in_executor(None, _run) # type: ignore
        except Exception as e:
            print(f"[M41][AWSALB-FORGE]: {e}")
        return None

    # ═══════════════════════════════════════════
    # M42: 3G network emulation (Playwright CDP)
    # ═══════════════════════════════════════════
    async def m42_3g_emulation(self, url: str, context: Any) -> Optional[str]:
        print("[M42][3G-EMUL]: Slow 3G network profile (more human-like timing)...")
        try:
            page = await context.new_page()
            try:
                cdp = await context.new_cdp_session(page)
                await cdp.send("Network.emulateNetworkConditions", {
                    "offline": False, "latency": 400,
                    "downloadThroughput": 1500000 // 8,
                    "uploadThroughput": 750000 // 8,
                    "connectionType": "cellular3g"
                })
            except Exception:
                pass
            bot = HumanBot(page)
            await page.goto("https://sol.du.ac.in/home.php",
                            wait_until="domcontentloaded", timeout=120000)
            await bot.read(random.uniform(3, 5))
            await page.goto(self.parent_url, wait_until="networkidle", timeout=120000)
            await bot.full_human_session(duration=15)
            response = await context.request.get(url, headers={
                "referer": self.parent_url,
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
            })
            await page.close()
            print(f"[M42][3G-EMUL]: {response.status}")
            if response.ok:
                return await response.text()
        except Exception as e:
            print(f"[M42][3G-EMUL]: {e}")
        return None

    # ═══════════════════════════════════════════
    # LEGACY: fetch_cffi (used by discover_and_crawl)
    # ═══════════════════════════════════════════
    async def fetch_cffi(self, url: str) -> Optional[str]:
        self.current_url = url
        if cffi_requests is None:
            # Fallback to plain requests
            try:
                r = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=20)
                return r.text if r.status_code == 200 else None
            except Exception:
                return None
        try:
            session = cffi_requests.Session(impersonate="chrome124") # type: ignore
            h = self._iframe_headers() if "vcs.php" in url else {"User-Agent": self.user_agent}
            r = session.get(url, headers=h, timeout=30)
            return r.text if r.status_code == 200 else None
        except Exception:
            return None

    async def fetch_wayback(self, url: str) -> Optional[str]:
        self.current_url = url
        return await self.m06_wayback(url)

    async def fetch_paid(self, url: str, provider: str) -> Optional[str]:
        self.current_url = url
        if provider == "SCRAPER_API":
            return await self.m23_scraperapi(url)
        elif provider == "ANT":
            return await self.m24_scraperант(url)
        elif provider == "WSAI":
            return await self.m25_wsai(url)
        return None

    # ═══════════════════════════════════════════
    # CRAWLER & DISCOVERY
    # ═══════════════════════════════════════════
    async def discover_and_crawl(self, max_pages: int = 50):
        """
        Full SOL website crawler — both subdomains:
          - sol.du.ac.in      (main portal, notices, all-notices)
          - web.sol.du.ac.in  (subdomain, student support, schedules)
        Follows all links with .php/.html/.pdf extensions.
        Deduplicates URLs. Skips already visited pages.
        """
        SOL_DOMAINS = ("sol.du.ac.in", "web.sol.du.ac.in")

        # Seed both subdomains if not already in queue
        extra_seeds = [
            "https://web.sol.du.ac.in/home",
            "https://web.sol.du.ac.in/info/student-support",
            "https://web.sol.du.ac.in/info/online-class-schedule",
            "https://sol.du.ac.in/all-notices.php",
            "https://sol.du.ac.in/home.php",
        ]
        for seed in extra_seeds:
            if seed not in self.visited and seed not in self.discovery_queue:
                self.discovery_queue.append(seed)

        print(f"[CRAWLER]: Starting full SOL website crawl (max {max_pages} pages)...")
        print(f"[CRAWLER]: Covering domains: {SOL_DOMAINS}")
        count = 0

        while self.discovery_queue and count < max_pages:
            url = self.discovery_queue.pop(0)
            if url in self.visited:
                continue
            self.visited.add(url)
            count += 1 # type: ignore
            print(f"[CRAWLER][{count}/{max_pages}]: {url}")

            html = await self.fetch_cffi(url)
            if not html:
                continue
            
            # CRITICAL: Skip BeautifulSoup if content is binary or a PDF
            # This prevents internal html.parser from crashing on binary junk charrefs
            if url.lower().endswith(".pdf") or html.startswith("%PDF-") or "\x00" in html:
                continue

            soup = BeautifulSoup(html, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"].strip()

                # Skip anchors, javascript, mailto
                if not href or href.startswith("#") or href.startswith("javascript") or href.startswith("mailto"):
                    continue

                # Resolve relative URLs — use the current page's domain as base
                if href.startswith("/"):
                    from urllib.parse import urlparse
                    parsed_base = urlparse(url)
                    href = f"{parsed_base.scheme}://{parsed_base.netloc}{href}"
                elif not href.startswith("http"):
                    href = self.base_url + "/" + href

                # Only follow SOL domain links
                if not any(domain in href for domain in SOL_DOMAINS):
                    continue

                # Avoid duplicates and already visited
                if href in self.visited or href in self.discovery_queue:
                    continue

                # Only queue pages likely to have content
                href_lower = href.lower()
                if any(ext in href_lower for ext in [".php", ".html", ".pdf", "/info/", "/notice", "/student", "/mba", "/schedule"]):
                    self.discovery_queue.append(href)

            # Parse and collect MBA items — skip binary PDFs
            self.current_url = url
            parsed = []
            if not url.lower().endswith(".pdf"):
                parsed = self._parse_html(html)
            
            for item in parsed:
                if not any(n["link"] == item["link"] for n in self.notices):
                    print(f"  [✔ FOUND]: {item['title']}")
                    self.notices.append(item)

    # ═══════════════════════════════════════════
    # CLASS CHAIN — All 42 methods in order
    # ═══════════════════════════════════════════
    async def run_class_chain(self) -> List[Dict[str, Any]]:
        print("\n[OMNI]: ═══ CLASS SCHEDULE CHAIN — 42 Methods ═══")
        urls = [
            self.class_schedule_url,
            "https://web.sol.du.ac.in/info/all-pg-class-time-table-sem-3-and-5"
        ]
        all_results = []
        
        for url in urls:
            self.current_url = url
            print(f"\n[CHAIN]: 🔍 Scanning {url}")
            url_success = False

            # ── Fast HTTP methods (no browser) ──
            fast_methods = [
                ("M01-CFFI",           lambda: self.m01_cffi(url)),
                ("M02-TLS-CLIENT",     lambda: self.m02_tls_client(url)),
                ("M03-HTTPX-H2",       lambda: self.m03_httpx(url)),
                ("M04-CLOUDSCRAPER",   lambda: self.m04_cloudscraper(url)),
                ("M05-COOKIES",        lambda: self.m05_manual_cookies(url)),
                ("M06-WAYBACK",        lambda: self.m06_wayback(url)),
                ("M07-CDX",            lambda: self.m07_cdx(url)),
                ("M08-GCACHE",         lambda: self.m08_google_cache(url)),
                ("M09-BING-CACHE",     lambda: self.m09_bing_cache(url)),
                ("M10-YANDEX",         lambda: self.m10_yandex_cache(url)),
                ("M11-COMMONCRAWL",    lambda: self.m11_commoncrawl(url)),
                ("M12-CACHEDVIEW",     lambda: self.m12_cachedview(url)),
                ("M13-CF-WORKER",      lambda: self.m13_cf_worker(url)),
                ("M14-VERCEL",         lambda: self.m14_vercel(url)),
                ("M15-NETLIFY",        lambda: self.m15_netlify(url)),
                ("M16-TOR",            lambda: self.m16_tor(url)),
                ("M17-I2P",            lambda: self.m17_i2p(url)),
                ("M18-FREEPROXY",      lambda: self.m18_freeproxy(url)),
                ("M19-IPv6",           lambda: self.m19_ipv6(url)),
                ("M20-DoH",            lambda: self.m20_doh(url)),
                ("M21-TIMING-JITTER",  lambda: self.m21_timing_jitter(url)),
                ("M22-CURL-IMPERSONATE", lambda: self.m22_curl_impersonate(url)),
                ("M24-SCRAPERАNT",     lambda: self.m24_scraperант(url)),
                ("M25-WSAI",           lambda: self.m25_wsai(url)),
                ("M23-SCRAPERAPI",     lambda: self.m23_scraperapi(url)),
                ("M41-AWSALB-FORGE",   lambda: self.m41_awsalb_forge(url)),
            ]

            for name, fn in fast_methods:
                print(f"  [CHAIN]: ── {name} ──")
                try:
                    html = await fn()
                    if html and self._is_valid(html): # type: ignore
                        res = self._parse_html(html)
                        if res:
                            print(f"  [CHAIN]: ✅ {name} SUCCESS — {len(res)} classes!")
                            all_results.extend(res)
                            url_success = True
                            break
                except Exception as e:
                    print(f"  [CHAIN]: {name} crashed — {e}")

            if url_success: continue

            # ── Playwright Chromium ──
            print(f"  [CHAIN]: ── Launching Playwright Chromium for {url} ──")
            try:
                async with async_playwright() as p:
                    is_mobile = random.choice([True, False])
                    ua = random.choice(self.mobile_agents if is_mobile else self.user_agents)
                    browser = await p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-dev-shm-usage",
                              "--disable-blink-features=AutomationControlled"]
                    )
                    context = await browser.new_context(
                        user_agent=ua,
                        viewport={"width": 390, "height": 844} if is_mobile
                        else {"width": 1366, "height": 768},
                        is_mobile=is_mobile, has_touch=is_mobile,
                        locale="en-IN", timezone_id="Asia/Kolkata",
                    )
                    await context.add_init_script(HumanBot.js_mask_script())

                    browser_methods = [
                        ("M26-PW-GHOST",  lambda: self.m26_pw_ghost(url, context)),
                        ("M27-PW-HUMAN",  lambda: self.m27_pw_human(url, context)),
                        ("M40-CSRF",      lambda: self.m40_csrf_cookies(url, context)),
                        ("M42-3G-EMUL",   lambda: self.m42_3g_emulation(url, context)),
                    ]
                    for name, fn in browser_methods:
                        print(f"    [CHAIN]: ── {name} ──")
                        try:
                            html = await fn()
                            if html and self._is_valid(html): # pyre-ignore[16]
                                res = self._parse_html(html) # pyre-ignore[16]
                                if res:
                                    print(f"    [CHAIN]: ✅ {name} SUCCESS — {len(res)} classes!")
                                    all_results.extend(res)
                                    url_success = True
                                    break
                        except Exception as e:
                            print(f"    [CHAIN]: {name} crashed — {e}")
                    await browser.close()
            except Exception as e:
                print(f"  [CHAIN]: Browser Manager failed — {e}")

        # ── Specialized browsers ──
        if not all_results:
            print("\n[CHAIN]: ── Specialized Browsers Fallback ──")
            # (Just doing first URL for specialized to save time unless all failed)
            url = urls[0] 
            specialized = [
                ("M28-PATCHRIGHT",    lambda: self.m28_patchright(url)),
                ("M29-NODRIVER",      lambda: self.m29_nodriver(url)),
                ("M30-CAMOUFOX",      lambda: self.m30_camoufox(url)),
                ("M31-SELENIUMBASE",  lambda: self.m31_seleniumbase(url)),
                ("M32-UCD",           lambda: self.m32_ucd(url)),
                ("M33-DRISSIONPAGE",  lambda: self.m33_drissionpage(url)),
                ("M34-PYDOLL",        lambda: self.m34_pydoll(url)),
                ("M35-SCRAPLING",     lambda: self.m35_scrapling(url)),
                ("M36-BOTASAURUS",    lambda: self.m36_botasaurus(url)),
                ("M37-SELENIUM-WIRE", lambda: self.m37_selenium_wire(url)),
                ("M38-PUPPETEER",     lambda: self.m38_puppeteer(url)),
                ("M39-PYCHROME",      lambda: self.m39_pychrome(url)),
            ]
            for name, fn in specialized:
                print(f"  [CHAIN]: ── {name} ──")
                try:
                    html = await fn()
                    if html and self._is_valid(html):
                        res = self._parse_html(html)
                        if res:
                            print(f"  [CHAIN]: ✅ {name} SUCCESS — {len(res)} classes!")
                            all_results.extend(res)
                            break
                except Exception as e:
                    print(f"  [CHAIN]: {name} crashed — {e}")

        return all_results


    # ═══════════════════════════════════════════
    # PARSING
    # ═══════════════════════════════════════════
    def _parse_html(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        results: List[Dict[str, Any]] = []
        is_home = "home.php" in self.current_url.lower() # pyre-ignore[16]

        if is_home:
            imp_div = soup.find(id="important-links")
            if imp_div:
                for a in imp_div.find_all("a", href=True):  # type: ignore
                    txt = a.get_text().strip()
                    if txt:
                        abs_link = urljoin(self.current_url, a["href"])
                        
                        # Use extracted date if available
                        e_date = self.extract_date_from_text(txt)
                        
                        if not e_date:
                            # Use persistent discovery date or today's date
                            e_date = self.discovery_dates.get(abs_link) or datetime.datetime.now().strftime("%Y-%m-%d")
                            self.discovery_dates[abs_link] = e_date
                        
                        results.append({
                            "title": ("MBA Update: " + re.sub(r'^\[.*?\]\s*', '', txt).strip())[:100], # type: ignore
                            "link": abs_link,
                            "semester": self.extract_semester_logic(txt),
                            "date": e_date,
                            "class_time": "", "description": "SOL Announcement"
                        })

        tables = soup.find_all("table")
        is_schedule = "vcs.php" in self.current_url.lower() # pyre-ignore[16]
        if is_schedule:
            print(f"  [DEBUG]: {len(tables)} tables on schedule page")

        for tidx, table in enumerate(tables):
            rows = table.find_all("tr")
            current_date: Optional[str] = None
            for row in rows:
                txt = row.get_text().lower()
                if "date:" in txt:
                    m = re.search(r"(\d{1,2}[-/]\d{2}[-/]\d{4})", txt)
                    if m:
                        current_date = m.group(1)
                        if is_schedule:
                            print(f"    [DEBUG]: Table {tidx} date: {current_date}")
                        continue
                if not current_date:
                    continue
                cells = row.find_all(["td", "th"])
                # Robust extraction: find subject and time by content instead of index
                subj = ""
                time_txt = ""
                sem_raw = ""
                teacher = "Unknown"
                
                # Sem/Year is usually cells[1]
                if len(cells) > 1: sem_raw = cells[1].get_text(strip=True)
                if len(cells) > 5: teacher = cells[5].get_text(strip=True)
                
                for idx, c in enumerate(cells):
                    txt = c.get_text(strip=True)
                    # Subject is usually cells[2]
                    if idx == 2 or (idx < 4 and not subj and len(txt) > 5 and ":" not in txt):
                        subj = txt
                    # Time pattern detection
                    if re.search(r"\d{1,2}:\d{2}", txt):
                        time_txt = txt
                
                if not any(kw.lower() in row.get_text().lower() for kw in self.keywords): # type: ignore
                    continue
                
                semester = self.extract_semester_logic(sem_raw) # type: ignore
                if semester == "0": semester = self.extract_semester_logic(subj) # type: ignore
                
                # v100.2: Clean subject title before saving
                clean_subj = self.cleanup_title(subj)
                
                raw_href = next(
                    (a["href"] for c in reversed(cells)
                     for a in [c.find("a")] if a and a.get("href")),
                    "#pending"
                )
                abs_link = urljoin(self.current_url, raw_href) if raw_href != "#pending" else "#pending" # type: ignore
                
                # Standardize date and parse
                clean_date = str(current_date).replace('/', '-')
                parsed_date = self.parse_date(clean_date)
                iso_scheduled = self.make_iso_scheduled(parsed_date, time_txt)
                
                results.append({
                    "title": f"[{clean_date}] MBA SEM {semester}: {clean_subj} ({time_txt})",
                    "link": abs_link, "semester": semester,
                    "date": parsed_date,
                    "class_time": time_txt,
                    "scheduledAt": iso_scheduled,
                    "description": f"MBA Live Class: {clean_subj} at {time_txt} (Teacher: {teacher})"
                })

        # General MBA links
        seen = {r["link"] for r in results}
        for a in soup.find_all("a", href=True):
            txt = a.get_text().strip()
            if txt and any(kw.lower() in txt.lower() for kw in self.keywords): 
                # v75.4: UNBLOCKED - Allowing all MBA updates
                # if any(bad in txt.lower() for bad in ["study material", "syllabus", "course structure", "merit list", "list of candidates"]):
                #     continue
                abs_link = urljoin(self.current_url, a["href"]) # pyre-ignore[16]
                if abs_link not in seen:
                    clean = re.sub(r"^\[.*?\]\s*", "", txt).strip()
                    
                    # Use extracted date if available
                    e_date = self.extract_date_from_text(txt)
                    
                    if not e_date:
                        # Use persistent discovery date or today's date
                        e_date = self.discovery_dates.get(abs_link) or datetime.datetime.now().strftime("%Y-%m-%d")
                        self.discovery_dates[abs_link] = e_date
                    
                    results.append({
                        "title": f"MBA Update: {clean}"[:100], # type: ignore
                        "link": abs_link,
                        "semester": self.extract_semester_logic(txt), # pyre-ignore[16]
                        "date": e_date,
                        "class_time": "", "description": "Latest MBA Resource"
                    })

        # v100.1: Final Filter - Remove anything blacklisted by keyword or URL
        final_filtered = []
        for item in results:
            title = item.get("title", "").lower()
            link = item.get("link", "").lower()
            
            # Check keywords
            if any(bad in title for bad in self.blacklist_keywords):
                print(f"  [BLACKLIST-KEY]: Skipping {item.get('title')[:40]}...")
                continue
            
            # Check links
            if any(bad in link for bad in self.blacklist_links):
                print(f"  [BLACKLIST-LINK]: Skipping {item.get('link')}...")
                continue
                
            final_filtered.append(item)
            
        results = final_filtered

        # Year filter
        filtered, seen_links = [], set()
        for item in results:
            # FIX: Don't deduplicate #pending links, they are placeholders for different classes
            link = item.get("link", "#pending")
            if link != "#pending" and link in seen_links:
                continue
            
            try:
                date_str = str(item.get("date", ""))
                if "-" in date_str:
                    yr_part = date_str.split("-")[0]
                    yr = int(yr_part)
                else:
                    yr = self.current_year
            except (ValueError, IndexError, TypeError):
                yr = self.current_year
            
            # v83.28: Allow current year, future years, and a 1-year past buffer (Current - 1)
            # This ensures 2025 data is allowed during 2026, but 2024 is blocked.
            if yr >= (self.current_year - 1):
                filtered.append(item)
                if link != "#pending":
                    seen_links.add(link)
        return filtered

    async def _extract_frames_html(self, page: Any) -> Optional[str]:
        """Extract raw HTML from page + all frames, return first valid one"""
        for ctx in [page] + list(page.frames):
            try:
                html = await ctx.content()
                if html and self._is_valid(html): # type: ignore
                    return html
            except Exception:
                continue
        return None

    def _parse_raw_tables(self, tables: List[Any]) -> List[Dict[str, Any]]:
        results = []
        total_rows_found = 0
        for table_data in tables:
            if not table_data: continue
            total_rows_found += len(table_data)
            for row_data in table_data:
                if not isinstance(row_data, dict): continue
                cells = row_data.get("cells", [])
                if len(cells) < 4: continue
                
                row_html = str(row_data.get("html", "")).lower()
                
                # Course | Year/Sem | Subject | Medium | Class Time | Teacher Name | Login to Join
                subj = ""
                time_txt = ""
                sem_raw = ""
                current_date = ""

                # Flexible Detection: Iterate through cells to find values
                for idx, c in enumerate(cells):
                    txt = str(c.get("text", "")).strip()
                    if not txt: continue
                    
                    if re.search(r"\d{1,2}[-/]\d{1,2}[-/]\d{4}", txt):
                        current_date = txt
                    elif re.search(r"SEM\s*[1-6]", txt.upper()):
                        sem_raw = txt
                    elif re.search(r"\d{1,2}:\d{2}", txt):
                        time_txt = txt
                    elif len(txt) > 5 and not subj and ":" not in txt:
                        # Subject is usually the first long text that isn't time/date
                        subj = txt

                # Fallback to defaults if flexible detection failed
                if not subj and len(cells) > 2: subj = cells[2]["text"]
                if not sem_raw and len(cells) > 1: sem_raw = cells[1]["text"]
                if not current_date: current_date = cells[0]["text"]
                if not time_txt and len(cells) > 4: time_txt = cells[4]["text"]

                semester = self.extract_semester_logic(sem_raw)
                if semester == "0": semester = self.extract_semester_logic(subj)
                
                # v100.2: Clean subject title before saving
                clean_subj = self.cleanup_title(subj)

                # Determine link: NUCLEAR OPTION (Expanded v100.2)
                href = "#pending"
                
                # Look for Teams or VCS links specifically in the whole row HTML
                m_teams = re.search(r'https://teams\.microsoft\.com/[^\s\'"]+', row_html)
                m_vcs = re.search(r'https?://[^\s\'"]+vcs\.php[^\s\'"]+', row_html)
                m_rel = re.search(r'/(?:my|info|auth)/[^\s\'"]+', row_html)
                m_join = re.search(r'href=["\']([^"\']*(?:login|join|teams|meeting)[^"\']*)["\']', row_html, re.I)
                
                if m_teams: href = m_teams.group(0)
                elif m_vcs: href = m_vcs.group(0)
                elif m_join: 
                    href = m_join.group(1)
                    if not href.startswith("http"):
                        href = urljoin("https://web.sol.du.ac.in", href)
                elif m_rel: 
                    href = m_rel.group(0)
                    if href.startswith("/"): href = "https://web.sol.du.ac.in" + href
                
                if href == "#pending":
                    # Fallback to Cell-by-cell extraction (Search specifically for 'Login' text)
                    for c in reversed(cells):
                        cell_html = str(c.get("html", "")).lower()
                        if "login" in cell_html or "join" in cell_html or "click" in cell_html:
                            h = str(c.get("href", "") or "")
                            cl = str(c.get("click", "") or "")
                            target = h if (h and "javascript" not in h) else cl
                            if target:
                                m_url = re.search(r"(?:https?://|/)[^\s'\"]+", target)
                                if m_url:
                                    href = m_url.group(0)
                                    if href.startswith("/"): href = "https://web.sol.du.ac.in" + href
                                    break
                
                if href != "#pending":
                    print(f"  [DEBUG-SUCCESS]: Found link for '{clean_subj}': {href[:60]}...")
                else:
                    print(f"  [DEBUG-WARN]: Still no link found for '{clean_subj}'.")
                
                # Standardize current_date and parse
                clean_date = str(current_date).replace('/', '-')
                parsed_date = self.parse_date(clean_date)
                iso_scheduled = self.make_iso_scheduled(parsed_date, time_txt)
                
                results.append({
                    "title": f"[{clean_date}] MBA SEM {semester}: {clean_subj} ({time_txt})",
                    "link": href, "semester": semester,
                    "date": parsed_date,
                    "class_time": time_txt,
                    "scheduledAt": iso_scheduled,
                    "description": f"MBA Live Class: {clean_subj} at {time_txt}"
                })
        print(f"[OMNI]: 📊 Scanned {total_rows_found} rows, Found {len(results)} valid MBA classes.")
        return results

    async def _extract_frames(self, page: Any) -> List[Dict[str, Any]]:
        all_raw = []
        for ctx in [page] + list(page.frames):
            try:
                data = await ctx.evaluate("""() => {
                    return Array.from(document.querySelectorAll('table')).map(t => {
                        return Array.from(t.querySelectorAll('tr')).map(tr => ({
                            cells: Array.from(tr.querySelectorAll('td,th')).map(c => ({
                                text: c.innerText.trim(),
                                href: (c.querySelector('a') || {}).href || null,
                                click: (c.querySelector('a') ? c.querySelector('a').getAttribute('onclick') : null) || (c.getAttribute('onclick') || null)
                            })),
                            html: tr.innerHTML
                        }));
                    });
                }""")
                if data:
                    all_raw.extend(data)
            except Exception:
                continue
        return self._parse_raw_tables(all_raw)

    def cleanup_title(self, title: str) -> str:
        """
        v100.2: Removes redundant MBA branding and duplicate words.
        Example: "MBA SEM 4: STRATEGY Strategic Management" -> "Strategic Management"
        """
        if not title: return ""
        
        # 1. Strip Leading Branding (case insensitive)
        # Matches: "MBA SEM 4: ", "Semester 2 - ", etc.
        clean = re.sub(r'^(?:MBA\s+)?(?:SEM(?:ESTER)?|YEAR|YR|PART|TERM)\s*(?:IV|III|II|I|[1-6])\s*[:\-]?\s*', '', title, flags=re.I)
        
        # 2. Strip Time Brackets (e.g. "(11:00 - 13:00)")
        clean = re.sub(r'\(\d{1,2}:\d{2}\s*.*?\)', '', clean).strip()
        
        # 3. Aggressive word-by-word deduplication (case-insensitive)
        words = clean.split()
        final_words = []
        for w in words:
            # Check if this word is essentially a repeat of the previous one (e.g. STRATEGY Strategic)
            w_norm = re.sub(r'[^A-Z]', '', w.upper())
            prev_norm = re.sub(r'[^A-Z]', '', final_words[-1].upper()) if final_words else ""
            
            # If current word is a substring of previous or vice versa (and they are long enough)
            if prev_norm and (w_norm in prev_norm or prev_norm in w_norm) and len(w_norm) > 3:
                continue
            
            if not final_words or final_words[-1].lower() != w.lower():
                final_words.append(w)
        
        # 3. CLEAN SUBJECT - UNIVERSAL WORD FILTER (v100.7)
        seen_norm = set()
        words = clean.split()
        final_words = []
        stopwords = {'AND', 'IN', 'OF', 'FOR', 'WITH', 'THE', 'BY', 'TO'}
        
        for w in words:
            norm = re.sub(r'[^A-Z]', '', w.upper())
            is_camel = bool(re.search(r'[a-z]', w))
            if len(norm) >= 2:
                if norm in seen_norm and not is_camel:
                    continue
                seen_norm.add(norm)
            final_words.append(w)
            
        while final_words:
            last = re.sub(r'[^A-Z]', '', final_words[-1].upper())
            if last in stopwords or len(last) < 2:
                final_words.pop()
            else:
                break

        cleaned = " ".join(final_words).strip(": ").strip()
        return cleaned.replace(" :", ":").strip(": ").strip()

    def extract_date_from_text(self, text: str) -> Optional[str]:
        """Extract DD.MM.YYYY, DD-MM-YYYY, or DD/MM/YYYY from text"""
        if not text: return None
        # Pattern 1: DD.MM.YYYY or DD-MM-YYYY or DD/MM/YYYY
        m = re.search(r"(\d{1,2})[-./](\d{1,2})[-./](\d{2,4})", text)
        if m:
            d, m, y = m.groups()
            if len(y) == 2: y = "20" + y # Assume 20xx
            try:
                dt = datetime.datetime(int(y), int(m), int(d))
                return dt.strftime("%Y-%m-%d")
            except Exception:
                pass
        return None

    def extract_semester_logic(self, text: str) -> str:
        if not text:
            return "0"
        # CLEANING: Remove any date patterns [YYYY-MM-DD], [DD-MM-YYYY], etc.
        cleaned_text = re.sub(r"\[?\d{1,4}[-/]\d{1,4}[-/]\d{1,4}\]?", "", text)
        t = cleaned_text.upper().replace("-", " ").replace(".", " ")
        if "1ST" in t or "FIRST" in t:
            return "1"
        if "2ND" in t or "SECOND" in t:
            return "2"
        if "3RD" in t or "THIRD" in t:
            return "3"
        if "4TH" in t or "FOURTH" in t:
            return "4"
        if "5TH" in t or "FIFTH" in t:
            return "5"
        roman = {"I": "1", "II": "2", "III": "3", "IV": "4", "V": "5"}
        m = re.search(r"(?:SEM(?:ESTER)?|YEAR|YR|PART|TERM)\s*(IV|III|II|I|[1-4])\b", t)
        if m:
            return roman.get(m.group(1), m.group(1))
        m = re.search(r"([1-4])(?:ST|ND|RD|TH)?\s*(?:SEM(?:ESTER)?|YEAR|YR|PART|TERM)", t)
        if m:
            return m.group(1)
        m = re.search(r"\b([1-4])(?:ST|ND|RD|TH)\b", t)
        if m:
            return m.group(1)
        m = re.search(r"MBA\s*(IV|III|II|I|[1-4])\b", t)
        if m:
            return roman.get(m.group(1), m.group(1))
        m = re.search(r"\b(IV|III|II|I)\b", t)
        if m:
            return roman[m.group(1)]
        m = re.search(r"\b([1-4])\b", t)
        if m:
            return m.group(1)
        return "0"

    def _is_valid(self, html: Any) -> bool:
        return bool(html and "sol" in str(html).lower() and len(str(html)) > 500)

    def parse_date(self, ds: str) -> str:
        for fmt in ["%d-%m-%Y", "%d/%m/%Y"]:
            try:
                return datetime.datetime.strptime(ds.strip(), fmt).strftime("%Y-%m-%d")
            except Exception:
                continue
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def _parse_time_to_dt(self, date_str: str, time_str: str) -> Optional[datetime.datetime]:
        if not date_str or not time_str: return None
        try:
            # Extract HH:MM and AM/PM
            m = re.search(r"(\d{1,2}):(\d{2})\s*(am|pm)?", time_str.lower())
            if not m: return None
            
            hh, mm, period = m.groups()
            hh, mm = int(hh), int(mm)
            
            # Handle Period/24h logic
            if period == 'pm' and hh < 12: 
                hh += 12
            elif period == 'am' and hh == 12: 
                hh = 0
            elif not period:
                # Heuristic for DU SOL: 
                # If it's already 24h (e.g. 15, 19), keep it.
                # If it's very low (1-7) without AM/PM, it's likely an evening class (e.g. "5:00" -> 17:00)
                if 1 <= hh <= 7: 
                    hh += 12
            
            # Parse date (expects YYYY-MM-DD)
            d_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return d_obj.replace(hour=hh, minute=mm, second=0, microsecond=0)
        except Exception:
            return None

    def extract_times(self, date_str: str, time_str: str) -> tuple[Optional[datetime.datetime], Optional[datetime.datetime]]:
        """Returns (start_dt, end_dt) from a date and a time string/title"""
        if not date_str or not time_str: return None, None
        try:
            # Handle formats like "17:00 - 19:00" or "02:00 PM to 04:00 PM"
            time_parts = re.split(r'-|to', time_str.lower())
            start_txt = time_parts[0].strip()
            end_txt = time_parts[1].strip() if len(time_parts) > 1 else None
            
            start_dt = self._parse_time_to_dt(date_str, start_txt)
            end_dt = self._parse_time_to_dt(date_str, end_txt) if end_txt else None
            
            # If no end time, default to start + 2 hours for cleanup safety
            if start_dt and not end_dt:
                end_dt = start_dt + datetime.timedelta(hours=2)
                
            return start_dt, end_dt
        except Exception:
            return None, None

    def make_iso_scheduled(self, date_str: str, time_str: str) -> Optional[str]:
        """Combine date (YYYY-MM-DD) and time (HH:MM AM/PM) into ISO format"""
        # We only use the START time for the official scheduledAt field
        start_txt = time_str.split("-")[0].strip()
        dt = self._parse_time_to_dt(date_str, start_txt)
        return dt.isoformat() if dt else None

    async def scrape_pg_timetables(self) -> List[Dict[str, Any]]:
        """
        Scrapes PG Time Tables via direct SOL JSON API (Browserless).
        """
        print("\n[OMNI]: ═══ PG TIME TABLE SCRAPER (API-DRIVEN) ═══")
        base_api = "https://web.sol.du.ac.in/my_modules/type/PG_TT_SESSION_25_26_SEM2_SEM_4/?operation=get_node"
        cdn_base = "https://web.sol.du.ac.in/my_modules/type/PG_TT_SESSION_25_26_SEM2_SEM_4/data/root/"
        
        folders = [
            ("1", "PG-TT-SEM-I-CLASS_"),
            ("2", "PG-TT-SEM-II-CLASS_"),
            ("3", "PG-TT-SEM-III-CLASS_"),
            ("4", "PG-TT-SEM-IV-CLASS_"),
            ("5", "PG-TT-SEM-V-CLASS_")
        ]
        
        results = []
        today = datetime.datetime.now()
        
        for sem_val, folder_id in folders:
            try:
                print(f"  [PG-API]: Fetching folder {folder_id}...")
                url = f"{base_api}&id={folder_id}"
                
                # Use simple requests since it's a JSON API
                loop = asyncio.get_event_loop()
                
                # Standard pattern to avoid lint errors with run_in_executor
                def _do_get(u, h):
                    return requests.get(u, headers=h, timeout=20, verify=False).json()
                
                nodes = await loop.run_in_executor(None, _do_get, url, {"User-Agent": self.user_agent})
                if not isinstance(nodes, list):
                    continue
                
                for node in nodes:
                    text = node.get("text", "").strip()
                    node_id = node.get("id", "")
                    
                    if "MBA" not in text.upper() or node.get("type") != "file":
                        continue
                        
                    # Extract Dates: "Dated 23.03.2026 to 28.03.2026" or "Dated 26.03.2026" or just "05.04.2026"
                    date_match = re.search(r"(?:Dated\s+)?(\d{2}\.\d{2}\.\d{4})(?:\s+to\s+(\d{2}\.\d{2}\.\d{4}))?", text, re.I)
                    if not date_match:
                        # Fallback: check for DD-MM-YYYY or any 8-10 digit date pattern
                        date_match = re.search(r"(\d{2}[-./]\d{2}[-./]\d{2,4})", text)
                        
                    if not date_match:
                        # Non-dated schedules (fallback to today or created_at)
                        start_str = today.strftime("%d.%m.%Y")
                        end_str = start_str
                    else:
                        start_str = date_match.group(1).replace('-', '.').replace('/', '.')
                        try:
                            end_str = date_match.group(2).replace('-', '.').replace('/', '.') if date_match.group(2) else start_str
                        except IndexError:
                            end_str = start_str
                    
                    try:
                        end_date = datetime.datetime.strptime(end_str, "%d.%m.%Y")
                        if today.date() > end_date.date():
                            continue
                    except Exception:
                        pass
                    
                    # Direct Link: Base + Encoded ID (SOL already encodes them usually)
                    # We ensure spaces are %20 just in case
                    final_id = node_id.replace(" ", "%20")
                    pdf_link = f"{cdn_base}{final_id}"
                    
                    results.append({
                        "title": f"[Timetable] MBA SEM {sem_val}: {text.replace('.pdf','').replace('.PDF','')}",
                        "link": pdf_link,
                        "semester": sem_val,
                        "date": datetime.datetime.strptime(start_str, "%d.%m.%Y").strftime("%Y-%m-%d"),
                        "description": f"Official PG Time Table valid until {end_str}. Direct PDF Link.",
                        "type": "notifications"
                    })
                    print(f"  [PG-API]: ✅ Success -> {text}")
            except Exception as e:
                print(f"  [PG-API]: Error in folder {folder_id} -> {e}")
                
        return results

    # ═══════════════════════════════════════════
    # MASTER RUN
    # ═══════════════════════════════════════════
    async def run(self: Any, days_back: int = 15, mode: str = "all",
                  targets: Optional[List[str]] = None) -> list:
        
        is_termux = os.environ.get("IS_TERMUX", "false").lower() == "true"
        
        if mode == "all":
            print(f"[OMNI]: COMPREHENSIVE scan (Classes + Notices + Discovery) | Termux mode: {is_termux}")
            
            # 1. PG Time Table (Now API-Driven, works on any host!)
            pg_tt = await self.scrape_pg_timetables()
            self.notices.extend(pg_tt)

            if is_termux:
                # ── Termux Exclusive: Heavy Browser Tasks ──
                # 2. Class Schedule Chain (vcs.php handles its own Playwright)
                self.notices.extend(await self.run_class_chain())
            else:
                print("[OMNI]: Non-Termux host. Skipping heavier Class Chain (delegated to phone).")
                # Remove schedule URL from crawler queue so it doesn't discover it
                if "https://web.sol.du.ac.in/info/online-class-schedule" in self.discovery_queue:
                    self.discovery_queue.remove("https://web.sol.du.ac.in/info/online-class-schedule")
            
            await self.discover_and_crawl(max_pages=1000)
            print(f"[SUMMARY]: Total MBA items: {len(self.notices)}")

        elif mode == "website":
            print("[OMNI]: WEBSITE & NOTICES scan")
            for url in ["https://sol.du.ac.in/all-notices.php", "https://sol.du.ac.in/home.php"]:
                html = await self.fetch_cffi(url)
                if html:
                    self.current_url = url
                    parsed = self._parse_html(html)
                    for item in parsed:
                        if not any(n["link"] == item["link"] for n in self.notices):
                            print(f"  [✔ FOUND]: {item['title']}")
                            self.notices.append(item)
            await self.discover_and_crawl(max_pages=1000)
            print(f"[SUMMARY]: {len(self.notices)} items found")

        elif mode == "classes":
            print("[OMNI]: CLASS SCHEDULE ONLY scan")
            self.notices.extend(await self.run_class_chain())

        # v73.9: Nuclear Reset for Blacklisted links (RECOVERY MODE)
        if len(self.dismissed_links) > 50:
            print(f"[OMNI]: ⚠️ Blacklist too large ({len(self.dismissed_links)}). Clearing to recover lost data.")
            self.dismissed_links = set()
            self._save_json(self.dismissed_file, list(self.dismissed_links))

        # v100.2: Save discovery dates for persistence
        self._save_json(self.discovery_file, self.discovery_dates)
        
        return self.notices

    # ═══════════════════════════════════════════
    # SYNC & CLEANUP
    # ═══════════════════════════════════════════
    def sync_results(self: Any, results: list, notifier: Any, memory_file: str, allow_deletions: bool = True):
        # 🚀 STRATEGY UPDATE: Scraper now uses Bulk Sync (Auto-Purge Mode).
        # It groups items by category and semester, then replaces the entire 
        # semester's data on the backend in one transaction. 
        # This ensures zero accumulation of outdated/duplicate items.
        
        print(f"[SYNC]: Syncing {len(results)} items to backend via Bulk Sync... | Deletions: {allow_deletions}")

        # 1. Group by Category and Semester
        groups = {
            "notifications": {},
            "live-classes": {}
        }
        
        def clean_subject(text):
            if not text: return ""
            # Strip [Date]
            text = re.sub(r'\[.*?\]', '', text)
            # Strip common prefixes
            for prefix in ["MBA Sem 1:", "MBA Sem 2:", "MBA Sem 3:", "MBA Sem 4:", "MBA Live Class:", "Live Class:", "Sem 1:", "Sem 2:", "Sem 3:", "Sem 4:"]:
                text = text.replace(prefix, "")
            # Strip everything before the last colon (often the subject is after the colon)
            if ":" in text:
                text = text.split(":")[-1]
            # Strip anything in parentheses like (2:00 PM - 3:00 PM)
            text = re.sub(r'\(.*?\)', '', text)
            return text.strip().lower()

        unique_check = set()
        clean_results = []
        for item in results:
            # Create a unique key based on title, date, AND link
            link = item.get("link", "#pending")
            u_key = f"{clean_subject(item.get('title'))}-{item.get('date')}-{link}"
            
            # ALLOW multiple placeholder links (#pending)
            if link != "#pending" and u_key in unique_check:
                print(f"  [SYNC-DEDUPE]: Skipping actual duplicate: {item.get('title')[:40]}")
                continue
            
            unique_check.add(u_key)
            clean_results.append(item)
        
        print(f"[SYNC]: Clean results (after deduplication): {len(clean_results)}")
        
        for item in clean_results:
            link = str(item.get("link", ""))
            title = str(item.get("title", ""))
            l_title = title.lower()
            l_desc = str(item.get("description", "")).lower()
            
            # CLASSIFICATION: 100% Bulletproof
            l_title = title.lower()
            l_desc = str(item.get("description", "")).lower()
            
            # If it has a Teams link, it IS a live class. Period.
            is_class = (
                "teams.microsoft" in link.lower() or
                item.get("type") == "live-classes" or
                item.get("class_time") or 
                "vcs.php" in link.lower() or
                re.search(r'\[\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\]', l_title) # Handle BOTH DD-MM and YYYY-MM
            )
            
            # Categorization: If it's a class (has Teams link or recognized as class), 
            # always put it in live-classes, even if the link is #pending.
            if is_class:
                category = "live-classes"
                print(f"  [SYNC-CLASS]: {title[:50]} -> link: {link}")
            else:
                category = "notifications"
                print(f"  [SYNC-NOTIF]: {title[:50]}")
                
            semester = str(item.get("semester", "0"))
            # HEALER: If semester is "0", try to find it in the title
            if semester == "0" and title:
                semester = self.extract_semester_logic(title)
                item["semester"] = semester # Persist healed value
            
            # v75.1: Instant End-Time Filtering (Skip for Timetables)
            if is_class and item.get("date") and "[Timetable]" not in title:
                now = datetime.datetime.now()
                _, end_dt = self.extract_times(item["date"], item.get("class_time") or title)
                if end_dt and end_dt < now:
                    print(f"  [SYNC-SKIP]: Class already ended today -> {title}")
                    continue
            
            # Ensure scheduledAt is set even if make_iso_scheduled failed (fallback to date only)
            if not item.get("scheduledAt") and item.get("date"):
                item["scheduledAt"] = f"{item['date']}T00:00:00"

            # Dual-sync logic: Classes go to BOTH live-classes and notifications
            # Notices go ONLY to notifications
            if semester not in groups["notifications"]:
                groups["notifications"][semester] = []
            
            if is_class:
                if semester not in groups["live-classes"]:
                    groups["live-classes"][semester] = []
                groups["live-classes"][semester].append(item)
                
                # Classes also appear in notifications feed (FORCE SYNC)
                groups["notifications"][semester].append(item)
                print(f"  [SYNC-DEBUG]: Adding {title[:30]} to NOTIFS group (Total: {len(groups['notifications'][semester])})")
            else:
                # Regular notices only in notifications
                groups["notifications"][semester].append(item)

        # 2. Perform Bulk Syncs
        stats = {"groups_synced": 0, "failed": 0, "deleted": 0}
        
        # Ensure all targeted semesters (0-4) are refreshed to purge stale data
        # Safety check: Force sync if we are in Termux or have enough data
        is_termux_env = os.environ.get("IS_TERMUX", "false").lower() == "true"
        if len(results) < 2 and not is_termux_env:
            print("[SYNC]: Insufficient data found. Skipping sync to prevent accidental wipe.")
            return

        target_semesters = ["0", "1", "2", "3", "4"]
        target_categories = ["notifications", "live-classes"]
        
        is_termux_env = os.environ.get("IS_TERMUX", "false").lower() == "true"

        for category in target_categories:
            for semester in target_semesters:
                items = groups[category].get(semester, []) # type: ignore

                if is_termux_env:
                    # TERMUX: Full authority - sync everything as-is
                    print(f"  [TERMUX-SYNC]: {category} Sem {semester} → {len(items)} items")
                    sync_deletions = allow_deletions
                    if not items and not sync_deletions:
                        print(f"[SYNC]: 🛡️ Skipping {category} SEM {semester} (empty + no-delete).")
                        continue
                else:
                    # NON-TERMUX (Render): Conservative - protect Termux data
                    sync_deletions = allow_deletions
                    
                    if category == "live-classes":
                        sync_deletions = False
                    
                    if category == "notifications" and semester in ["1", "2", "3", "4"]:
                        sync_deletions = False
                    
                    # Merge protected items from existing backend feed
                    if category == "notifications":
                        existing_notifs = notifier.get_from_website(semester)
                        if existing_notifs:
                            protected = [
                                n for n in existing_notifs
                                if (n.get("description") and "MBA Live Class" in n["description"]) or
                                   (n.get("link") and ("teams.microsoft" in n["link"] or "vcs.php" in n["link"]))
                            ]
                            for ep in protected:
                                if not any(str(n.get("link")) == str(ep.get("link")) for n in items):
                                    items.append(ep)
                    
                    if not items and not sync_deletions:
                        print(f"[SYNC]: 🛡️ Skipping {category} SEM {semester} (empty, non-Termux).")
                        continue

                # v75.7: MODAL PROTECTION
                # If we are only syncing classes, we MUST NOT delete regular notifications.
                if category == "notifications" and getattr(self, "target_mode", "all") == "classes":
                    sync_deletions = False
                    print(f"  [GUARD]: Classes-only mode detected. Disabling deletions for NOTIFICATIONS.")

                if notifier.bulk_sync_to_website(category, semester, items, allow_deletions=sync_deletions):
                    stats["groups_synced"] += 1 # type: ignore
                else:
                    stats["failed"] += 1 # type: ignore


        # v73.9: Manual Dismissal & Restore Detection
        # If an item was in our history (synced_ids.json) but is MISSING from the 
        # backend, it means an Admin deleted it. We add it to dismissed_links.json
        # so we don't re-add it in the next crawl.
        history = self._load_json(memory_file, set)
        backend_items_all = []
        for sem in ["0", "1", "2", "3", "4"]:
            b_data = notifier.get_from_website(sem)
            if b_data: backend_items_all.extend(b_data)
        
        backend_links = {str(b.get("link", "")) for b in backend_items_all}
        
        c_stats = {"dismissed": 0, "restored": 0}
        
        # Disable automatic blacklisting for now to prevent "Joining Session" links from being accidentally banned
        # for old_link in history:
        #     old_link_str = str(old_link)
        #     if old_link_str not in backend_links and old_link_str != "#pending":
        #         was_in_current_scrape = any(str(r.get("link")) == old_link_str for r in results)
        #         if was_in_current_scrape and old_link_str not in self.dismissed_links:
        #             print(f"  [DISMISS]: Blacklisting link: {old_link_str}")
        #             self.dismissed_links.add(old_link_str)
        #             c_stats["dismissed"] = c_stats["dismissed"] + 1
        
        # 2. Detect Manual RESTORES (Blacklisted link -> Now present in backend)
        # If an admin manually adds it back, remove it from the blacklist.
        links_to_restore = []
        for bl_link in self.dismissed_links:
            if str(bl_link) in backend_links:
                links_to_restore.append(bl_link)
        
        for r_link in links_to_restore:
            print(f"  [RESTORE]: Unblocking link: {str(r_link)}")
            self.dismissed_links.remove(r_link)
            c_stats["restored"] = c_stats["restored"] + 1
        
        if c_stats["dismissed"] or c_stats["restored"]:
            self._save_json(self.dismissed_file, self.dismissed_links)

        # Update history with current scrape
        current_links = {str(r.get("link", "")) for r in results if r.get("link") and r["link"] != "#pending"}
        history.update(current_links)
        self._save_json(memory_file, history)

        print(f"[SYNC]: Done. {stats['groups_synced']} category/semester groups refreshed.")

        # 3. Legacy Deletion Logic (Optional - Bulk sync handles purge automatically)
        if len(results) > 2:
            print("[SYNC]: Checking for deletions (Items removed from SOL)...")
            scrape_links = {r["link"] for r in results if r.get("link") and r["link"] != "#pending"}
            for sem in ["1", "2", "3", "4"]: # Class-specific semesters
                backend_items = notifier.get_from_website(sem)
                if not backend_items: continue
                for b_item in backend_items:
                    b_link = b_item.get("link")
                    b_id = b_item.get("_id") or b_item.get("id")
                    # ✅ SAFETY: Only delete if link is missing AND it's a ROOT item (no folderId)
                    # This prevents deleting Recorded Classes that have been moved to folders.
                    if b_link and b_link != "#pending" and not b_item.get("folderId") and b_link not in scrape_links:
                        # Extra check: Only delete if date is still current/future
                        # (Past dates are handled by cleanup_old_data anyway)
                        print(f"  [SYNC-DELETE]: Item removed from SOL -> {b_item.get('title')[:50]}")
                        if notifier.delete_from_website(sem, b_id):
                            stats["deleted"] += 1 # type: ignore
                            # Remove from local synced_ids too
                            # (But we don't have the hash here, so we'll just let it re-add if it ever reappears)

        print(f"[SYNC]: GroupsSynced={stats['groups_synced']} Deleted={stats['deleted']} Failed={stats['failed']}") # type: ignore

    def cleanup_old_data(self: Any, notifier: Any):
        print("[CLEANUP]: Auto-cleanup old records...")
        now = datetime.datetime.now()
        thirty_ago = now - datetime.timedelta(days=30)
        for sem in ["0", "1", "2", "3", "4"]:
            items = notifier.get_from_website(sem)
            if not items:
                continue
            deleted = 0
            for item in items:
                item_id = item.get("_id") or item.get("id")
                if not item_id:
                    continue
                try:
                    item_date = datetime.datetime.strptime(
                        item.get("date", ""), "%Y-%m-%d"
                    )
                    # ✅ SAFETY: Never auto-delete items inside folders (Recorded Classes)
                    # v89.2: Aggressive Timetable Expiration
                    to_delete = False
                    if not is_in_folder:
                        # 1. Check title for specific expiry (e.g. "Dated 18.04")
                        title = item.get("title", "").lower()
                        dates = re.findall(r'(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{2,4})', title)
                        if dates:
                            # Use the LAST date found in title as expiry
                            d, m, y = dates[-1]
                            if len(y) == 2: y = "20" + y
                            expiry_date = datetime.date(int(y), int(m), int(d))
                            if now.date() > expiry_date:
                                to_delete = True
                                print(f"  [CLEANUP]: Expiring item by title date ({expiry_date}) -> {title[:40]}")
                        
                        # 2. Fallback to general date-based cleanup
                        if not to_delete:
                            if sem == "0":
                                if item_date < thirty_ago: to_delete = True
                            else:
                                # Standard items expire after 1 day
                                if item_date.date() < (now - datetime.timedelta(days=1)).date():
                                    to_delete = True
                    
                    if to_delete and notifier.delete_from_website(sem, item_id):
                        deleted += 1 # type: ignore
                except Exception as e:
                    print(f"  [CLEANUP-ERR]: {e}")
                    continue
            if deleted:
                print(f"  [CLEANUP]: Sem {sem} — deleted {deleted} expired items")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    SCRAPER_KEY = os.environ.get("SCRAPER_KEY", "")
    BACKEND_URL = os.environ.get("BACKEND_URL", "https://solmates-backend-w27e.onrender.com")

    async def standalone_run():
        mode = "all"
        if "--mode" in sys.argv:
            idx = sys.argv.index("--mode")
            if idx + 1 < len(sys.argv):
                mode = sys.argv[idx + 1]
        force = "--force" in sys.argv or os.environ.get("FORCE_SYNC", "").lower() == "true"

        scraper = MBAScraper(target_mode=mode, force_sync=force)
        results = await scraper.run(mode=mode)
        if results:
            try:
                notifier = Notifier(BACKEND_URL, SCRAPER_KEY)
                scraper.sync_results(results, notifier, "synced_ids.json")
                # v83.27: Disabled redundant standalone cleanup to let backend handle Smart Purge
                # if mode == "all":
                #     scraper.cleanup_old_data(notifier)
                print(f"[OMNI]: Scan ({mode}) complete.")
            except NameError:
                print("[ERROR]: Notifier not found. Sync skipped.")
        else:
            print(f"[OMNI]: No items for mode '{mode}'.")

    asyncio.run(standalone_run())
