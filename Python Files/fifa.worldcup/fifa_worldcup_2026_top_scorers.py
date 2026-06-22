import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics/player-statistics"
FILE_NAME = "fifa_worldcup_2026_top_scorers.json"

def fetch_top_scorers():
    print("⚽ Starting FIFA World Cup 2026 Top Scorers Scraper...")
   
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1600,1200")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
   
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
   
    try:
        print(f"Loading player statistics page: {URL}")
        driver.get(URL)
       
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(5)
       
        # Load more if available
        try:
            load_more = driver.find_element(By.XPATH, "//button[contains(text(), 'Load more')]")
            if load_more.is_displayed():
                print("Loading more players...")
                driver.execute_script("arguments[0].click();", load_more)
                time.sleep(6)
        except:
            pass
       
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
       
        if not table:
            print("❌ Could not find statistics table.")
            return
       
        scorers = []
        rows = table.find_all('tr')[1:]
        print(f"📊 Found {len(rows)} player rows...")
       
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 4:
                continue
                
            # Rank
            rank_text = cols[0].get_text(strip=True)
            try:
                rank = int(rank_text)
            except:
                rank = rank_text
                
            # Player cell
            player_cell = cols[1]
            raw_text = player_cell.get_text(separator=" ", strip=True)
            
            # Find all images
            images = player_cell.find_all('img')
            headshot_url = ""
            flag_url = ""
            
            for img in images:
                src = img.get('src', '')
                if not src:
                    continue
                full_url = src if src.startswith('http') else f"https://www.fifa.com{src}"
                
                # Headshot is usually larger or has player name in URL
                if 'height:850' in src or 'crop,height' in src or 'UNDAV' in src or len(src) > 100:
                    headshot_url = full_url
                else:
                    # Everything else is likely the flag
                    flag_url = full_url
            
            # Fallback: first image = headshot, second = flag
            if not headshot_url and images:
                src = images[0].get('src', '')
                headshot_url = src if src.startswith('http') else f"https://www.fifa.com{src}"
            if not flag_url and len(images) > 1:
                src = images[1].get('src', '')
                flag_url = src if src.startswith('http') else f"https://www.fifa.com{src}"
            
            # Parse name, country, position
            parts = raw_text.split()
            player_name_parts = []
            country = ""
            position = ""
            
            i = 0
            while i < len(parts):
                part = parts[i]
                if len(part) == 3 and part.isupper() and not country:
                    country = part
                    i += 1
                    continue
                elif len(part) == 2 and part.isupper() and country:
                    position = part
                    i += 1
                    continue
                elif not country:
                    player_name_parts.append(part)
                i += 1
            
            player_name = " ".join(player_name_parts).strip()
            
            # Goals, Assists, Minutes
            goals = cols[2].get_text(strip=True)
            assists = cols[3].get_text(strip=True) if len(cols) > 3 else ""
            minutes = cols[4].get_text(strip=True) if len(cols) > 4 else ""
            
            scorers.append({
                "rank": rank,
                "player": player_name,
                "country": country,
                "position": position,
                "headshot_url": headshot_url,
                "flag_url": flag_url,
                "goals": goals,
                "assists": assists,
                "minutes_played": minutes
            })
        
        # Save
        output_data = {
            "tournament": "FIFA World Cup 2026",
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_players": len(scorers),
            "top_scorers": scorers
        }
        
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
           
        print(f"✅ SUCCESS! Generated {FILE_NAME} with {len(scorers)} players.")
        if scorers:
            print(f"Sample: {scorers[0]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_top_scorers()
