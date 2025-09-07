from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

# Konfigurasi Chrome
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_argument("--headless")  # Hapus ini kalau mau lihat browser

# Inisialisasi driver
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
    print("⚠️ Player tidak muncul dalam 30 detik")

# Tambahan delay untuk XHR
time.sleep(10)

# Log semua request ke file debug
with open("debug_requests.txt", "w") as log:
    for request in driver.requests:
        if request.response:
            log.write(request.url + "\n")

# Cari URL .mpd
stream_url = None
for request in driver.requests:
    if request.response and ".mpd" in request.url:
        stream_url = request.url
        break

# Tutup browser
driver.quit()

# Simpan hasil ke latest.txt
with open("latest.txt", "w") as f:
    if stream_url:
        print("✅ Stream ditemukan:", stream_url)
        f.write(stream_url + "\n")
    else:
        print("❌ Tidak ditemukan stream .mpd")
        f.write("#ERROR: Stream .mpd tidak ditemukan\n")

    f.write("Updated at: " + datetime.now().isoformat())
