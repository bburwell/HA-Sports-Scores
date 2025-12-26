import urllib.request
import json

API_URL = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20251210-20260215"

# YOUR FULLY VERIFIED bowlseason.com LOGO MAP (2025-26 season)
BOWL_NAME_MAP = {
    # NON-PLAYOFF BOWLS (41)
    "Cricket Celebration Bowl": "https://bowlseason.com/images/2025/6/4/Celebration_Bowl__Website_.png?width=80&height=80&mode=max",
    "Bucked Up LA Bowl": "https://bowlseason.com/images/2025/9/30/LA_Bowl_Logo.png?width=80&height=80&mode=max",
    "IS4S Salute to Veterans Bowl": "https://bowlseason.com/images/2024/10/14/IS4S_Salute_to_Veterans_Bowl.png?width=80&height=80&mode=max",
    "StaffDNA Cure Bowl": "https://bowlseason.com/images/2024/6/6/2024_StaffDNA_Cure_Bowl_Ehx0h.png?width=80&height=80&mode=max",
    "68 Ventures Bowl": "https://bowlseason.com/images/2023/6/14/68_Ventures_Bowl__Light_BG_.png?width=80&height=80&mode=max",
    "Xbox Bowl": "https://bowlseason.com/images/2025/12/4/XBox_Bowl_Logo.PNG?width=80&height=80&mode=max",
    "Myrtle Beach Bowl": "https://bowlseason.com/images/2025/11/6/Myrtle_Beach_Bowl_Presented_by_Engine.png?width=80&height=80&mode=max",
    "Union Home Mortgage Gasparilla Bowl": "https://bowlseason.com/images/2024/12/3/Union_Home_Mortgage_Gasparilla_Bowl_2024.png?width=80&height=80&mode=max",
    "Famous Idaho Potato Bowl": "https://bowlseason.com/images/2020/11/2/famous_idaho_potato_bowl.png?width=80&height=80&mode=max",
    "Boca Raton Bowl": "https://bowlseason.com/images/2025/11/20/Bush_s_Boca_Raton_Bowl.png?width=80&height=80&mode=max",
    "New Orleans Bowl": "https://bowlseason.com/images/2025/12/4/NewOrleansBowl_Logo_01A_woMSr.png?width=80&height=80&mode=max",
    "Scooter's Coffee Frisco Bowl": "https://bowlseason.com/images/2023/8/7/Scooter_s_Coffee_Frisco_Bowl.png?width=80&height=80&mode=max",
    "Sheraton Hawai\u02bbi Bowl": "https://bowlseason.com/images/2025/6/4/Sheraton_Hawai_i_Bowl_Logo_25.png?width=80&height=80&mode=max",
    "GameAbove Sports Bowl": "https://bowlseason.com/images/2024/10/8/GameAbove_Sports_Bowl_Logo.png?width=80&height=80&mode=max",
    "Rate Bowl": "https://bowlseason.com/images/2024/10/17/Rate_Bowl_CMYK-logo.png?width=80&height=80&mode=max",
    "SERVPRO First Responder Bowl": "https://bowlseason.com/images/2021/11/4/SERVPRO_First_Responder_Bowl_Logo.png?width=80&height=80&mode=max",
    "Go Bowling Military Bowl": "https://bowlseason.com/images/2024/6/6/24_302_GB_Military_Bowl_Logo_CMYK.png?width=80&height=80&mode=max",
    "Bad Boy Mowers Pinstripe Bowl": "https://bowlseason.com/images/2022/8/16/Bad_Boy_Mowers_Pinstripe_Bowl_Logo.png?width=80&height=80&mode=max",
    "Wasabi Fenway Bowl": "https://bowlseason.com/images/2021/11/3/Wasabi_Fenway_Bowl_Logo_Primary.png?width=80&height=80&mode=max",
    "Pop-Tarts Bowl": "https://bowlseason.com/images/2023/5/30/Pop-Tarts_Bowl.png?width=80&height=80&mode=max",
    "Snoop Dogg Arizona Bowl": "https://bowlseason.com/images/2024/6/6/Snoop_Dogg_Arizona_Bowl.png?width=80&height=80&mode=max",
    "Isleta New Mexico Bowl": "https://bowlseason.com/images/2025/6/4/Isleta_New_Mexico_Bowl_-_20th_Anniversary.png?width=80&height=80&mode=max",
    "TaxSlayer Gator Bowl": "https://bowlseason.com/images/2020/11/2/TaxSlayer_Gator_Bowl_Logo.png?width=80&height=80&mode=max",
    "Kinder's Texas Bowl": "https://bowlseason.com/images/2024/12/4/Kinder_s_Texas_Bowl.png?width=80&height=80&mode=max",
    "JLab Birmingham Bowl": "https://bowlseason.com/images/2025/9/19/JLab_Birmingham_Bowl.png?width=80&height=80&mode=max",
    "Radiance Technologies Independence Bowl": "https://bowlseason.com/images/2020/11/2/Radiance_Logo_Small.png?width=80&height=80&mode=max",
    "Liberty Mutual Music City Bowl": "https://bowlseason.com/images/2025/10/20/LMMCB_Logo_CLR.png?width=80&height=80&mode=max",
    "Valero Alamo Bowl": "https://bowlseason.com/images/2018/12/20/VAB_logo_1_.png?width=80&height=80&mode=max",
    "ReliaQuest Bowl": "https://bowlseason.com/images/2025/6/4/ReliaQuest_Bowl-40th_Anniversary__Silver_.png?width=80&height=80&mode=max",
    "Tony the Tiger Sun Bowl": "https://bowlseason.com/images/2020/11/2/Sun_Bowl_Logo_71.png?width=80&height=80&mode=max",
    "Cheez-It Citrus Bowl": "https://bowlseason.com/images/2022/11/15/Cheez-It_Citrus_Bowl_Logo_MfPJc.png?width=80&height=80&mode=max",
    "SRS Distribution Las Vegas Bowl": "https://bowlseason.com/images/2024/6/6/SRS_Distribution_Las_Vegas_Bowl.png?width=80&height=80&mode=max",
    "Goodyear Cotton Bowl Classic": "https://bowlseason.com/images/2020/11/2/Cotton_Bowl_logo_svg.png?width=80&height=80&mode=max",
    "Capital One Orange Bowl": "https://bowlseason.com/images/2017/11/8/orange.png?width=80&height=80&mode=max",
    "Rose Bowl Game Presented by Prudential": "https://bowlseason.com/images/2023/1/1/Rose_Bowl_Game-Prudential_Logo.png?width=80&height=80&mode=max",
    "Allstate Sugar Bowl": "https://bowlseason.com/images/2022/9/14/Allstate_Sugar_Bowl_2022_Logo.png?width=80&height=80&mode=max",
    "Lockheed Martin Armed Forces Bowl": "https://bowlseason.com/images/2025/8/28/Armed_Forces_Bowl_2025.png?width=80&height=80&mode=max",
    "AutoZone Liberty Bowl": "https://bowlseason.com/images/2020/11/2/AZLB_Logo_2019_PNG_Color.png?width=80&height=80&mode=max",
    "Holiday Bowl": "https://bowlseason.com/images/2023/5/31/Holiday_Bowl.png?width=80&height=80&mode=max",
    "Duke's Mayo Bowl": "https://bowlseason.com/images/2020/11/2/dukes_logo.png?width=80&height=80&mode=max",
    "Vrbo Fiesta Bowl": "https://bowlseason.com/images/2023/5/31/Vrbo_Fiesta_Bowl_Logo.png?width=80&height=80&mode=max",
    "Chick-fil-A Peach Bowl": "https://bowlseason.com/images/2020/11/2/1200px_Peach_Bowl_logo_svg.png?width=80&height=80&mode=max",
    "East-West Shrine Bowl": "https://bowlseason.com/images/2023/12/14/Asset_13_4x.png?width=80&height=80&mode=max",
    "Panini Senior Bowl": "https://bowlseason.com/images/2025/8/7/Panini_Senior_Bowl.png?width=80&height=80&mode=max",
    "R+L Carriers New Orleans Bowl": "https://bowlseason.com/images/2025/6/4/New_Orleans_Bowl.png?width=80&height=80&mode=max",
    "DirectTV Holiday Bowl": "https://bowlseason.com/images/2023/5/31/Holiday_Bowl.png?width=80&height=80&mode=max",

    # CFP (7)
    "College Football Playoff First Round Game": "https://bowlseason.com/images/2024/9/27/CFP_STACK_COL_FIRST_ROUND.png?width=80&height=80&mode=max",
    "College Football Playoff Quarterfinal at the Goodyear Cotton Bowl Classic": "https://bowlseason.com/images/2020/11/2/Cotton_Bowl_logo_svg.png?width=80&height=80&mode=max",
    "College Football Playoff Quarterfinal at the Capital One Orange Bowl": "https://bowlseason.com/images/2017/11/8/orange.png?width=80&height=80&mode=max",
    "College Football Playoff Quarterfinal at the Rose Bowl Presented by Prudential": "https://bowlseason.com/images/2023/1/1/Rose_Bowl_Game-Prudential_Logo.png?width=80&height=80&mode=max",
    "College Football Playoff Quarterfinal at the Allstate Sugar Bowl": "https://bowlseason.com/images/2022/9/14/Allstate_Sugar_Bowl_2022_Logo.png?width=80&height=80&mode=max",
    "College Football Playoff Semifinal at the Chick-fil-A Peach Bowl": "https://bowlseason.com/images/2020/11/2/1200px_Peach_Bowl_logo_svg.png?width=80&height=80&mode=max",
    "College Football Playoff Semifinal at the Vrbo Fiesta Bowl": "https://bowlseason.com/images/2023/5/31/Vrbo_Fiesta_Bowl_Logo.png?width=80&height=80&mode=max",
    "College Football Playoff National Championship Presented by AT&T": "https://bowlseason.com/images/2022/12/6/CFP_VERT_NC_MARK_LT_BG.png?width=80&height=80&mode=max",
}

CONFERENCE_MAP = {
    "1":   "ACC",
    "4":   "Big 12",
    "5":   "Big Ten",
    "8":   "SEC",
    "9":   "Pac-12",
    "12":  "C-USA",
    "15":  "MAC",
    "16":  "WAC",
    "17":  "Mountain West",
    "18":  "FBS Independent",
    "20":  "Big Sky",
    "21":  "MVFC",
    "22":  "Ivy",
    "24":  "MEAC",
    "25":  "NEC",
    "26":  "OVC",
    "27":  "Patriot",
    "28":  "Pioneer",
    "29":  "Southern",
    "30":  "Southland",
    "31":  "SWAC",
    "37":  "Sun Belt",
    "40":  "Big South",
    "151": "American",  # Updated from "ASUN" based on ESPN data (e.g., AAC for teams like Army)
    "176": "OVC-Big South",
    "179": "Big South-OVC",
    # Add more if needed
}

def fetch_data():
    try:
        response = urllib.request.urlopen(API_URL, timeout=30)
        return json.loads(response.read())
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"events": []}

def is_bowl_game(event):
    for comp in event.get("competitions", []):
        for note in comp.get("notes", []):
            h = note.get("headline", "")
            if "Bowl" in h and "Playoff" not in h and "Championship" not in h:
                return True
    return False

def is_cfp_playoff(event):
    keywords = ["CFP", "Playoff", "Semifinal", "First Round", "Quarterfinal"]
    for comp in event.get("competitions", []):
        for note in comp.get("notes", []):
            if any(k in note.get("headline", "") for k in keywords):
                return True
    return False

def is_championship(event):
    for comp in event.get("competitions", []):
        for note in comp.get("notes", []):
            if "Championship" in note.get("headline", ""):
                return True
    return False

def add_conferences_to_teams(event):
    for comp in event.get("competitions", []):
        for competitor in comp.get("competitors", []):
            team = competitor.get("team", {})
            if not team:
                continue
            # ESPN usually puts conferenceId in team.conferenceId
            conf_id = team.get("conferenceId")
            if conf_id and conf_id in CONFERENCE_MAP:
                team["conference"] = CONFERENCE_MAP[conf_id]
            else:
                # Fallback: sometimes it's under group.id
                conf_id = team.get("group", {}).get("id")
                if conf_id and conf_id in CONFERENCE_MAP:
                    team["conference"] = CONFERENCE_MAP[conf_id]
                else:
                    team["conference"] = "Unknown"

def is_any_bowl(event):
    return is_bowl_game(event) or is_cfp_playoff(event) or is_championship(event)

def get_bowl_image_url(event):
    try:
        headline = event["competitions"][0]["notes"][0]["headline"]
    except (IndexError, KeyError, TypeError):
        headline = ""

    # Direct match from your verified map
    if headline in BOWL_NAME_MAP:
        return BOWL_NAME_MAP[headline]

    # Fallback generic
    return "https://bowlseason.com/images/2025/6/4/Celebration_Bowl__Website_.png?width=80&height=80&mode=max"

def add_bowl_images(events, filename):
    for event in events:
        event["bowl_image"] = get_bowl_image_url(event)
        add_conferences_to_teams(event)  # ← this adds conference to each team's object
    save_json(filename, events)

def save_json(filename, data):
    with open(f"/config/www/{filename}", "w") as f:
        json.dump({"events": data}, f, indent=2)
    print(f"Saved {filename}")

if __name__ == "__main__":
    print("Fetching 2025-26 bowl data...")
    data = fetch_data()
    events = data.get("events", [])

    all_bowls = [e for e in events if is_any_bowl(e)]
    regular_bowls = [e for e in events if is_bowl_game(e)]
    playoffs = [e for e in events if is_cfp_playoff(e)]
    championship = [e for e in events if is_championship(e)]

    add_bowl_images(all_bowls, "cfb_all_bowls.json")
    add_bowl_images(regular_bowls, "cfb_regular_bowls.json")
    add_bowl_images(playoffs, "cfb_cfp_playoffs.json")
    add_bowl_images(championship, "cfb_championship.json")

    print("All done! Real bowlseason.com logos added.")
