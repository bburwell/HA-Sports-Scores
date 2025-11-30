import urllib.request
import json

API_URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20251210-20260131"
#2024-2025 Season - "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20241210-20250215"

def fetch_data():
    response = urllib.request.urlopen(API_URL)
    return json.loads(response.read())
    
# def is_any_bowl(event):
    # comp = event.get("competitions", [{}])[0]
    # is_post = comp.get("type", {}).get("abbreviation") == "post"

    # return is_post or is_cfp_playoff(event) or is_championship(event)
    
def is_bowl_game(event):
    # Check all notes across all competitions
    for comp in event.get("competitions", []):
        notes = comp.get("notes", [])
        for note in notes:
            headline = note.get("headline", "")
            if "Bowl" in headline and "Playoff" not in headline and "Championship" not in headline:
                return True
    return False




def is_cfp_playoff(event):
    keywords = ["CFP", "Playoff", "Semifinal", "First Round", "Quarterfinal"]
    for comp in event.get("competitions", []):
        notes = comp.get("notes", [])
        if notes:
            headline = notes[0].get("headline", "")
            if any(k in headline for k in keywords):
                return True
    return False

def is_championship(event):
    for comp in event.get("competitions", []):
        notes = comp.get("notes", [])
        if notes:
            headline = notes[0].get("headline", "")
            if "Championship" in headline:
                return True
    return False

# def is_bowl_game(event):
    # # Regular bowls are postseason but not CFP playoff rounds
    # comp = event.get("competitions", [{}])[0]
    # if comp.get("type", {}).get("abbreviation") == "post" and not is_cfp_playoff(event) and not is_championship(event):
        # return True
    # return False
    
def is_bowl_game(event):
    # Check all notes across all competitions
    for comp in event.get("competitions", []):
        notes = comp.get("notes", [])
        for note in notes:
            headline = note.get("headline", "")
            if "Bowl" in headline and "Playoff" not in headline and "Championship" not in headline:
                return True
    return False


def is_any_bowl(event):
    # A bowl is either a regular bowl, a CFP playoff, or a championship
    return is_bowl_game(event) or is_cfp_playoff(event) or is_championship(event)



def save_json(filename, data):
    with open(f"/config/www/{filename}", "w") as file:		
		#/config/www/
        json.dump({"events": data}, file, indent=2)
    #print(f"Saved {filename}")

if __name__ == "__main__":
    print("Fetching CFB Bowl data...")
    data = fetch_data()
    events = data.get("events", [])
    
    all_bowls = [e for e in events if is_any_bowl(e)]
    regular_bowls = [e for e in events if is_bowl_game(e)]
    playoffs = [e for e in events if is_cfp_playoff(e)]
    championship = [e for e in events if is_championship(e)]

    save_json("cfb_all_bowls.json", all_bowls)
    save_json("cfb_regular_bowls.json", regular_bowls)
    save_json("cfb_cfp_playoffs.json", playoffs)
    save_json("cfb_championship.json", championship)

    #print("Completed!")
