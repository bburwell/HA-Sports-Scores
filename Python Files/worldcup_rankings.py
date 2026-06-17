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
FILE_NAME = "fifa_rankings.json"

def fetch_all_211_rankings():
    print("Starting automated browser instance...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1600,1200")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print(f"Loading direct path layout: {URL}")
        driver.get(URL)
        
        # Explicit wait for the main data table wrapper to materialize
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(3)

        # 1. Fire an explicit text-based locator action on the "+ Show full rankings" wrapper
        try:
            print("Locating expansion anchor element...")
            expand_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Show full rankings')]"))
            )
            
            # FIXED: Correct array indexing syntax for Selenium execution arguments
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expand_btn)
            time.sleep(1)
            
            # FIXED: Correct array indexing syntax for the JavaScript click method
            driver.execute_script("arguments[0].click();", expand_btn)
            print("Expansion triggered successfully! Waiting for all rows to load...")
            time.sleep(6)  
            
        except Exception as btn_err:
            print(f"Could not interact with expansion button: {btn_err}")

        # 2. Extract and hand the fully expanded DOM to BeautifulSoup
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print("Error: Could not locate ranking table after running expansion click.")
            return

        rankings_list = []
        rows = table.find_all('tr')[1:] # Drop headers
        print(f"Analyzing data rows... Found {len(rows)} elements.")

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                # Isolate Rank
                rank_text = cells[0].text.strip()
                
                # Isolate Team Name safely from long form responsive layout text elements
                team_node = row.find('span', class_='d-none d-lg-block') or cells[1]
                team_name = team_node.text.strip()
                
                # Filter out the recent match history clutter completely.
                # Points are strictly numerical decimals (like 1735.77).
                points_text = ""
                for cell in cells[2:]:
                    text_clean = cell.text.strip()
                    # Check if string matches numerical floats without characters/words
                    if text_clean.replace('.', '', 1).isdigit() and '.' in text_clean:
                        points_text = text_clean
                        break
                
                # Check for empty fallback logic
                if not points_text and len(cells) >= 5:
                    points_text = cells[-2].text.strip()

                if team_name and team_name not in [t['team'] for t in rankings_list]:
                    rankings_list.append({
                        "rank": int(rank_text) if rank_text.isdigit() else rank_text,
                        "team": team_name,
                        "points": points_text
                    })

        # 3. Assemble and save the target schema cleanly
        if rankings_list:
            output_data = {
                "sport": "Soccer",
                "rankings": rankings_list
            }

            with open(FILE_NAME, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            print(f"Successfully generated {FILE_NAME} containing {len(rankings_list)} records!")
        else:
            print("Data extraction loop yielded empty arrays.")

    except Exception as e:
        print(f"Browser processing exception: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_all_211_rankings()
