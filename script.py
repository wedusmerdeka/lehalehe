from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import uuid

# Setup Chrome options
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--headless=new")  # Aktifkan headless untuk CI
options.add_argument(f"--user-data-dir=/tmp/chrome-profile-{uuid.uuid4()}")

# Setup Chrome driver via webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Buka halaman MNCTV
driver.get("https://www.rctiplus.com/tv/mnctv")
time.sleep(10)  # Tunggu player termuat

# Inject JS ke JW Player untuk ambil stream URL
try:
    stream_url = driver.execute_script("""
        try {
            return jwplayer().getPlaylistItem().file;
        } catch (e) {
            return null;
        }
    """)
except Exception as e:
    print("⚠️ Gagal inject JW API:", e)
    stream_url = None

driver.quit()

# Simpan hasil ke latest.txt
if stream_url:
    print("✅ Stream ditemukan:", stream_url)
    with open("latest.txt", "w") as f:
        f.write(stream_url)
else:
    print("❌ Tidak ditemukan stream dari JW Player")
    with open("latest.txt", "w") as f:
        f.write("#ERROR: Stream tidak ditemukan")
