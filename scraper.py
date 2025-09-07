import shutil
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Cari binary Chrome/Chromium
binary_path = shutil.which("google-chrome") or shutil.which("chromium-browser")
if not binary_path:
    raise FileNotFoundError("Google Chrome/Chromium tidak ditemukan.")

# Konfigurasi Chrome Options
options = Options()
options.binary_location = binary_path
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--window-size=1920,1080")

# Path Chromedriver
chromedriver_path = shutil.which("chromedriver")
if not chromedriver_path:
    raise FileNotFoundError("Chromedriver tidak ditemukan.")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Ganti URL ini dengan halaman player Vidio yang memuat stream target
    page_url = "https://www.vidio.com/live/205"
    driver.get(page_url)

    # Tunggu agar semua request termuat
    time.sleep(8)

    mpd_url = None
    for request in driver.requests:
        if request.response and ".mpd" in request.url and "hdntl=" in request.url:
            mpd_url = request.url
            break

    if mpd_url:
        print("MPD URL ditemukan:", mpd_url)
    else:
        print("MPD URL tidak ditemukan.")

finally:
    driver.quit()
