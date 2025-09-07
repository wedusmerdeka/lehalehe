from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Konfigurasi Chrome untuk lingkungan headless (GitHub Actions friendly)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")

# Inisialisasi driver dengan selenium-wire
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Buka halaman Vidio Indosiar
target_url = "https://www.vidio.com/live/205-indosiar"
driver.get(target_url)
time.sleep(15)  # Tunggu agar XHR selesai

# Cari URL .mpd dari semua request
stream_url = None
for request in driver.requests:
    if request.response:
        if ".mpd" in request.url and "akamaized.net" in request.url:
            stream_url = request.url
            break

# Tutup browser
driver.quit()

# Simpan hasil ke file
output_path = os.path.join(os.getcwd(), "latest.txt")
with open(output_path, "w") as f:
    if stream_url:
        print("✅ Stream ditemukan:", stream_url)
        f.write(stream_url)
    else:
        print("❌ Tidak ditemukan stream .mpd")
        f.write("#ERROR: Stream .mpd tidak ditemukan")
