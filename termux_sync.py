import os
import time
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[TERMUX-SYNC] %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

import importlib

def check_and_install_deps():
    """Ensure all required dependencies are installed in Termux."""
    required_packages = ["requests", "httpx", "beautifulsoup4", "python-dotenv", "nest-asyncio"]
    
    logger.info("Checking dependencies...")
    for pkg in required_packages:
        module_name = pkg.replace("-", "_")
        try:
            importlib.import_module(module_name)
        except ImportError:
            logger.info(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            logger.info(f"{pkg} installed successfully.")

def run_sync():
    """Execute the scraper and sync with backend."""
    try:
        import importlib.util
        # Move to the script's directory and add to path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Identity flag for scraper.py
        os.environ["IS_TERMUX"] = "true"
        # Prevent Android Doze from suspending the process
        os.system("termux-wake-lock > /dev/null 2>&1")
        
        # Dynamically load the main module
        # Check both current dir and subdirectory
        main_path = os.path.join(script_dir, 'main.py')
        if not os.path.exists(main_path):
            main_path = os.path.join(script_dir, 'mba_scraper', 'main.py')
            
        if not os.path.exists(main_path):
            logger.error(f"Scraper core (main.py) not found at {main_path} or {os.path.join(script_dir, 'main.py')}")
            return

        spec = importlib.util.spec_from_file_location("mba_main", main_path)
        if spec is None or spec.loader is None:
            logger.error(f"Failed to load spec for {main_path}")
            return
            
        mba_main = importlib.util.module_from_spec(spec) # type: ignore
        spec.loader.exec_module(mba_main)
        main_job = getattr(mba_main, 'main_job', None)
        
        if not main_job:
            logger.error("main_job not found in scraper core")
            return
        
        logger.info("Starting synchronization job (Additive Mode)...")
        # Set allow_deletions=False so Termux only supplements Render scraper
        main_job(mode="all", allow_deletions=False)
        logger.info("Synchronization completed successfully.")
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")

def main():
    logger.info("=== SOLMATES TERMUX AUTO-SYNC STARTING ===")
    
    # 1. Self-Setup
    try:
        check_and_install_deps()
    except Exception as e:
        logger.error(f"Dependency installation failed: {e}")
        logger.info("Please run 'pkg install python' and 'pip install requests' manually if this persists.")
    
    # 2. Infinite Loop
    while True:
        logger.info("--- Cycle Starting ---")
        run_sync()
        
        wait_time = 3600 # 1 hour
        logger.info(f"Cycle finished. Waiting {wait_time/60:.0f} minutes for next run...")
        time.sleep(wait_time)

if __name__ == "__main__":
    main()
