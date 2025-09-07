import shutil
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Cari binary Chrome/Chromium
binary_path = shutil.which("google-chrome") or shutil.which("chromium-browser") or shutil.which("chromium")
if not binary_path:
    raise FileNotFoundError("Chrome/Chromium tidak ditemukan di sistem.")

# Cari Chromedriver
chromedriver_path = shutil.which("chromedriver")
if not chromedriver_path:
    raise FileNotFoundError("Chromedriver tidak ditemukan di sistem.")

# Set Chrome options
options = Options()
options.binary_location = binary_path
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36")

# Start driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

print(f"✅ Chrome jalan di: {binary_path}")
driver.quit()
