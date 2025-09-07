from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")

# Gunakan WebDriver Manager untuk otomatis install versi yang cocok
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.vidio.com/live/205-indosiar")
time.sleep(15)

stream_url = None
for request in driver.requests:
    if request.response and ".mpd" in request.url and "akamaized.net" in request.url:
        stream_url = request.url
        break

driver.quit()

with open("latest.txt", "w") as f:
    f.write(stream_url if stream_url else "#ERROR: Stream .mpd tidak ditemukan")
