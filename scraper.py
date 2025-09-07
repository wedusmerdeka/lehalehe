import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Cari binary Chrome/Chromium yang tersedia
binary_path = shutil.which("google-chrome") or shutil.which("chromium-browser")
if not binary_path:
    raise FileNotFoundError("Google Chrome atau Chromium tidak ditemukan di sistem.")

# Konfigurasi Chrome Options
options = Options()
options.binary_location = binary_path
options.add_argument("--headless=new")  # Headless mode (versi baru)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Path ke chromedriver
chromedriver_path = shutil.which("chromedriver")
if not chromedriver_path:
    raise FileNotFoundError("Chromedriver tidak ditemukan di sistem.")

# Setup driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Contoh: buka halaman target
    url = "https://example.com"
    driver.get(url)

    # Tunggu sebentar untuk load
    time.sleep(2)

    # Contoh ambil judul halaman
    print("Page title:", driver.title)

    # Contoh ambil elemen
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    for idx, h1 in enumerate(h1_elements, start=1):
        print(f"H1-{idx}:", h1.text)

finally:
    driver.quit()
