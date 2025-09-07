from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Setup Chrome
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Buka halaman Vidio
driver.get("https://www.vidio.com/live/205-indosiar")

# Tunggu sampai player muncul
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "vidio-player"))
    )
except:
    print("⚠️ Player tidak muncul")

time.sleep(10)  # Tambahan delay agar XHR muncul

# Tangkap stream .mpd
stream_url = None
for request in driver.requests:
    if request.response and ".mpd" in request.url:
        stream_url = request.url
        break

driver.quit()

# Simpan ke latest.txt
with open("latest.txt", "w") as f:
    if stream_url:
        print("✅ Stream ditemukan:", stream_url)
        f.write(stream_url + "\n")
    else:
        print("❌ Tidak ditemukan stream .mpd")
        f.write("#ERROR: Stream .mpd tidak ditemukan\n")

    f.write("Updated at: " + datetime.now().isoformat())
