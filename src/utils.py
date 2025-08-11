import os, time, random, logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def build_driver(headless: bool = False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def sleep_with_jitter(minutes: int, jitter_sec: int = 60):
    # Sleep minutes +/- up to jitter_sec
    base = minutes * 60
    delta = random.randint(-jitter_sec, jitter_sec)
    total = max(5, base + delta)  # never less than 5 seconds
    time.sleep(total)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    return logging.getLogger("itu-course-taker")
