from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

# Konfigurasi Chrome
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--headless")  # Hapus ini kalau mau lihat browser
options.add_argument("--window-size=1920,1080")

# Inisialisasi driver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Buka halaman Vidio Indosiar
driver.get("https://www.vidio.com/live/205-indosiar")

# Tunggu agar XHR selesai
time.sleep(15)

# Cari URL .mpd dari semua request
stream_url = None
for request in driver.requests:
    if request.response and ".mpd" in request.url:
        stream_url = request.url
        break

# Tutup browser
driver.quit()

# Simpan hasil ke file
with open("latest.txt", "w") as f:
    if stream_url:
        print("✅ Stream ditemukan:", stream_url)
        f.write(stream_url + "\n")
    else:
        print("❌ Tidak ditemukan stream .mpd")
        f.write("#ERROR: Stream .mpd tidak ditemukan\n")

    # Tambahkan timestamp agar file selalu berubah
    f.write("Updated at: " + datetime.now().isoformat())
