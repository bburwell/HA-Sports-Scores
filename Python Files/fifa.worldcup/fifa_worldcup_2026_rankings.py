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

URL = "https://inside.fifa.com/fifa-world-ranking/men"
FILE_NAME = "fifa_worldcup_2026_rankings.json"

def fetch_all_211_rankings():
    print("🏆 Starting FIFA World Rankings Scraper with Flags...")
   
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1600,1200")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
   
    try:
        print(f"Loading official FIFA rankings page: {URL}")
        driver.get(URL)
       
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(3)
       
        # Click "Show full rankings"
        try:
            print("Expanding full 211-team table...")
            expand_btn = WebDriverWait(driver, 12).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Show full rankings')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expand_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", expand_btn)
            print("✅ Full rankings expanded! Waiting...")
            time.sleep(8)
        except Exception as btn_err:
            print(f"⚠️ Could not click expansion button: {btn_err}")
       
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
       
        if not table:
            print("❌ Error: Could not locate ranking table.")
            return
       
        rankings_list = []
        rows = table.find_all('tr')[1:]  # Skip header
        print(f"📊 Analyzing {len(rows)} ranking rows...")
       
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 6:
                continue
                
            # === RANK + CHANGE ===
            rank_cell = cells[0]
            rank_cell_text = rank_cell.get_text(separator=" ", strip=True)
            parts = rank_cell_text.split()
            try:
                rank_num = int(parts[0])
                change = int(parts[1]) if len(parts) > 1 else 0
            except (ValueError, IndexError):
                numbers = [int(t.strip()) for t in rank_cell.stripped_strings if t.strip().lstrip('-').isdigit()]
                rank_num = numbers[0] if numbers else 0
                change = numbers[1] if len(numbers) > 1 else 0
            
            # Team name + Flag
            team_node = row.find('span', class_='d-none d-lg-block') or cells[1]
            team_name = team_node.get_text(strip=True)
            
            # Find flag image (usually first img in the team cell)
            flag_img = row.find('img')
            flag_url = ""
            if flag_img and flag_img.get('src'):
                src = flag_img.get('src')
                flag_url = src if src.startswith('http') else f"https://inside.fifa.com{src}"
            
            # === POINTS ===
            points_change = ""
            total_points = ""
            for cell in cells:
                text = cell.get_text(strip=True)
                if not text:
                    continue
                if ('+' in text or '-' in text) and '.' in text and len(text) < 10:
                    points_change = text
                elif '.' in text and any(c.isdigit() for c in text) and len(text) > 6:
                    total_points = text
            
            if not total_points and len(cells) >= 6:
                total_points = cells[-2].get_text(strip=True)
            
            if team_name and team_name not in [t.get('team') for t in rankings_list]:
                rankings_list.append({
                    "rank": rank_num,
                    "change": change,
                    "team": team_name,
                    "flag_url": flag_url,           # ← New: JPEG/PNG link
                    "points_change": points_change,
                    "total_points": total_points
                })
        
        # Save
        if rankings_list:
            output_data = {
                "sport": "Soccer",
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_teams": len(rankings_list),
                "rankings": rankings_list
            }
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            print(f"✅ SUCCESS! Generated {FILE_NAME} with {len(rankings_list)} teams!")
            print(f"Sample with flag: {rankings_list[0]}")
        else:
            print("❌ No data extracted.")
            
    except Exception as e:
        print(f"❌ Browser error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_all_211_rankings()
