from seleniumwire import webdriver
import time

options = {
    'disable_encoding': True
}
driver = webdriver.Chrome(seleniumwire_options=options)
driver.get("https://www.vidio.com/live/205-indosiar")
time.sleep(5)  # Tunggu JS load

token = None
for request in driver.requests:
    if request.response and ".mpd" in request.url and "hdntl=" in request.url:
        token = request.url.split("hdntl=")[-1]
        break

driver.quit()

if token:
    with open("token.txt", "w") as f:
        f.write(token)
    print("✅ Token saved:", token)
else:
    print("❌ Token not found")
