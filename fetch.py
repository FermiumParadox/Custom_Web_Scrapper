from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import csv
from datetime import datetime

options = Options()

# 🔥 KEY FIX: don't wait for full load (ads/scripts)
options.page_load_strategy = "eager"

driver = webdriver.Chrome(options=options)

print("🚀 Opening page...")

driver.get("https://www.gamespot.com/articles/2026-upcoming-games-release-schedule/1100-6534941/")

print("✅ Page loaded (eager mode)")

time.sleep(3)

# scroll a bit
driver.execute_script("window.scrollTo(0, 1000);")
time.sleep(2)

body = driver.find_element(By.TAG_NAME, "body")
text = body.text

print("\n📄 TEXT PREVIEW:\n")
print(text[:1000])


lines = text.split("\n")

games = []

for line in lines:
    line = line.strip()

    # only keep lines that look like game entries
    if "(" in line and "-" in line:
        match = re.match(r"(.+?) \((.+?)\) - (.+)", line)

        if match:
            games.append({
                "name": match.group(1),
                "platform": match.group(2),
                "release_date": match.group(3)
            })

# show first 10 results
print("\n🎮 EXTRACTED GAMES:\n")

for g in games[:10]:
    print(g)

print(f"\n✅ Total games found: {len(games)}")

cleaned_games = []
seen = set()

for g in games:
    name = g["name"].strip()
    platform = g["platform"].strip()
    date = g["release_date"].strip()

    key = (name, platform, date)

    if key not in seen:
        seen.add(key)

        cleaned_games.append({
            "name": name,
            "platform": platform,
            "release_date": date
        })

print(f"✅ Cleaned games count: {len(cleaned_games)}")

def parse_date(date_str):
    try:
        # assume year 2026
        return datetime.strptime(date_str + " 2026", "%B %d %Y")
    except:
        return datetime.max  # push unknown dates to bottom


cleaned_games.sort(key=lambda x: parse_date(x["release_date"]))

# save the file
with open("games_2026.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "platform", "release_date"])

    writer.writeheader()
    writer.writerows(cleaned_games)

print("\n📁 File saved as games_2026.csv")