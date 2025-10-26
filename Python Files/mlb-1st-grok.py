import urllib.request
import json
from datetime import datetime, timezone

# Define the API URL for fetching MLB playoff data
#2024 MLB Playoffs API_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20241001-20241030"
API_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates=20250929-20251031"

def fetch_and_filter_data(region):
    try:
        response = urllib.request.urlopen(API_URL)
        data = json.loads(response.read())
        filtered_events = [
            event for event in data.get('events', [])
            if any(
                competition.get('notes') and region in competition['notes'][0].get('headline', '')
                for competition in event.get('competitions', [])
            )
        ]
        return {"events": filtered_events}
    except Exception as e:
        print(f"Error fetching data for {region}: {e}")
        return {"events": []}

def extract_round_name(notes_headline):
    if not notes_headline:
        return "Unknown Round"
    parts = notes_headline.split(" - ")
    for part in parts:
        if "Wild Card" in part or "ALWC" in part or "NLWC" in part:
            return "Wild Card"
        elif "Division Series" in part:
            return "Division Series"
        elif "Championship Series" in part:
            return "Championship Series"
        elif "World Series" in part:
            return "World Series"
        elif "First Round" in part:
            return "First Round"
        elif "Semifinals" in part:
            return "Semifinals"
        elif "Conference Finals" in part:
            return "Conference Finals"
        elif "Finals" in part:
            return "Finals"
        elif "Stanley Cup Final" in part:
            return "Stanley Cup Final"
    return "Unknown Round"

def create_series_structure(data):
    series_dict = {}
    team_abbr_to_name = {}

    for event in data.get('events', []):
        for competition in event.get('competitions', []):
            team1 = competition['competitors'][0]['team']
            team2 = competition['competitors'][1]['team']

            team_abbr_to_name[team1['abbreviation']] = team1['displayName']
            team_abbr_to_name[team2['abbreviation']] = team2['displayName']

            seed1 = competition['competitors'][0].get('seed', float('inf'))
            seed2 = competition['competitors'][1].get('seed', float('inf'))
            if seed1 < seed2:
                lowest_seed, highest_seed = team1, team2
            else:
                lowest_seed, highest_seed = team2, team1

            base_series_title = " vs ".join(sorted([lowest_seed['displayName'], highest_seed['displayName']]))
            notes_headline = competition.get('notes', [{}])[0].get('headline', '')
            round_name = extract_round_name(notes_headline)
            series_title = f"{base_series_title} ({round_name})"

            if series_title not in series_dict:
                series_dict[series_title] = {
                    "seriesTitle": series_title,
                    "seriesStatus": "0-0",
                    "seriesDetails": {
                        "Teams": [lowest_seed['displayName'], highest_seed['displayName']],
                        "seriesGames": [],
                        "maxGames": 7  # Default value
                    }
                }

            # Set maxGames for the series
            series_info = competition.get('series', {})
            max_games = series_info.get('totalCompetitions', 7)
            series_dict[series_title]["seriesDetails"]["maxGames"] = max_games

            status_info = competition.get('status', {})
            game_status = "scheduled"
            game_segment = None
            time_remaining = None
            if status_info.get('type', {}).get('completed', False):
                game_status = "final"
            elif status_info.get('type', {}).get('state') == "in":
                game_status = "live"
                inning_num = status_info.get('period', 0)
                if inning_num <= 9:
                    game_segment = f"{inning_num}{'st' if inning_num == 1 else 'nd' if inning_num == 2 else 'rd' if inning_num == 3 else 'th'}"
                else:
                    game_segment = "Extra Innings"
                time_remaining = status_info.get('displayClock', '0:00')

            odds_data = competition.get('odds', [])
            odds_details = {}
            if game_status == "scheduled" and odds_data:
                odds = odds_data[0]
                odds_details = {
                    "PointSpread": odds.get('details', 'N/A'),
                    "MoneylineHome": odds.get('homeTeamOdds', {}).get('moneyLine', 'N/A'),
                    "MoneylineAway": odds.get('awayTeamOdds', {}).get('moneyLine', 'N/A'),
                    "OverUnder": odds.get('overUnder', 'N/A')
                }
            else:
                odds_details = {
                    "PointSpread": "N/A",
                    "MoneylineHome": "N/A",
                    "MoneylineAway": "N/A",
                    "OverUnder": "N/A"
                }

            game_details = {
                "sport": "MLB",
                "gameNumber": len(series_dict[series_title]["seriesDetails"]["seriesGames"]) + 1,
                "Date": competition.get('date', 'TBD'),
                "Lowest Seed": {
                    "Name": lowest_seed['displayName'],
                    "Score": competition['competitors'][0].get('score', '0') if seed1 < seed2 else competition['competitors'][1].get('score', '0'),
                    "Logo": lowest_seed.get('logo', '')
                },
                "Highest Seed": {
                    "Name": highest_seed['displayName'],
                    "Score": competition['competitors'][1].get('score', '0') if seed1 < seed2 else competition['competitors'][0].get('score', '0'),
                    "Logo": highest_seed.get('logo', '')
                },
                "Broadcast": ", ".join(
                    broadcast.get('names', ['TBD'])[0]
                    for broadcast in competition.get('broadcasts', [])
                ),
                "Status": game_status,
                "GameSegment": game_segment,
                "TimeRemaining": time_remaining,
                "Odds": odds_details
            }
            series_dict[series_title]["seriesDetails"]["seriesGames"].append(game_details)

            series_dict[series_title]["latest_series_info"] = series_info

    # Update seriesStatus for each series
    for series_title, series in series_dict.items():
        series_info = series.get("latest_series_info", {})
        team1 = series["seriesDetails"]["Teams"][0]
        team2 = series["seriesDetails"]["Teams"][1]

        series_completed = series_info.get('completed', False)
        series_summary = series_info.get('summary', '')

        if series_completed and series_summary:
            if "wins" in series_summary.lower():
                winner_abbr = series_summary.split()[0]
                winner = team_abbr_to_name.get(winner_abbr, winner_abbr)
                wins = series_summary.split()[-1]
                series["seriesStatus"] = f"{winner} wins series {wins}"
            else:
                team1_wins = 0
                team2_wins = 0
                for game in series["seriesDetails"]["seriesGames"]:
                    try:
                        team1_score = int(game["Lowest Seed"]["Score"]) if game["Lowest Seed"]["Name"] == team1 else int(game["Highest Seed"]["Score"])
                        team2_score = int(game["Highest Seed"]["Score"]) if game["Highest Seed"]["Name"] == team2 else int(game["Lowest Seed"]["Score"])
                    except ValueError:
                        team1_score = 0
                        team2_score = 0

                    if team1_score > team2_score and team1_score != 0:
                        team1_wins += 1
                    elif team2_score > team1_score and team2_score != 0:
                        team2_wins += 1

                if team1_wins > team2_wins:
                    series["seriesStatus"] = f"{team1} wins series {team1_wins}-{team2_wins}"
                elif team2_wins > team1_wins:
                    series["seriesStatus"] = f"{team2} wins series {team2_wins}-{team1_wins}"
                else:
                    series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"
        elif series_summary:
            if "leads" in series_summary.lower():
                leader_abbr = series_summary.split()[0]
                leader = team_abbr_to_name.get(leader_abbr, leader_abbr)
                wins = series_summary.split()[-1]
                series["seriesStatus"] = f"{leader} leads series {wins}"
            else:
                team1_wins = 0
                team2_wins = 0
                for game in series["seriesDetails"]["seriesGames"]:
                    try:
                        team1_score = int(game["Lowest Seed"]["Score"]) if game["Lowest Seed"]["Name"] == team1 else int(game["Highest Seed"]["Score"])
                        team2_score = int(game["Highest Seed"]["Score"]) if game["Highest Seed"]["Name"] == team2 else int(game["Lowest Seed"]["Score"])
                    except ValueError:
                        team1_score = 0
                        team2_score = 0

                    if team1_score > team2_score and team1_score != 0:
                        team1_wins += 1
                    elif team2_score > team1_score and team2_score != 0:
                        team2_wins += 1

                if team1_wins > team2_wins:
                    series["seriesStatus"] = f"{team1} leads series {team1_wins}-{team2_wins}"
                elif team2_wins > team1_wins:
                    series["seriesStatus"] = f"{team2} leads series {team2_wins}-{team1_wins}"
                else:
                    series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"
        else:
            team1_wins = 0
            team2_wins = 0
            for game in series["seriesDetails"]["seriesGames"]:
                try:
                    team1_score = int(game["Lowest Seed"]["Score"]) if game["Lowest Seed"]["Name"] == team1 else int(game["Highest Seed"]["Score"])
                    team2_score = int(game["Highest Seed"]["Score"]) if game["Highest Seed"]["Name"] == team2 else int(game["Lowest Seed"]["Score"])
                except ValueError:
                    team1_score = 0
                    team2_score = 0

                if team1_score > team2_score and team1_score != 0:
                    team1_wins += 1
                elif team2_score > team1_score and team2_score != 0:
                    team2_wins += 1

            if team1_wins > team2_wins:
                series["seriesStatus"] = f"{team1} leads series {team1_wins}-{team2_wins}"
            elif team2_wins > team1_wins:
                series["seriesStatus"] = f"{team2} leads series {team2_wins}-{team1_wins}"
            else:
                series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"

        del series["latest_series_info"]

    return series_dict

def merge_original_and_series(data, series):
    return {
        "sport": "MLB",
        "events": data.get("events", []),
        "series": list(series.values())
    }

def save_to_file(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

if __name__ == "__main__":
    print("Fetching MLB playoff data...")
    playoff_rounds = [
        ("ALWC", "mlb_al_wild_card_gpt.json"),
        ("NLWC", "mlb_nl_wild_card_gpt.json"),
        ("ALDS", "mlb_al_division_series_gpt.json"),
        ("NLDS", "mlb_nl_division_series_gpt.json"),
        ("ALCS", "mlb_al_championship_series_gpt.json"),
        ("NLCS", "mlb_nl_championship_series_gpt.json"),
        ("World Series", "mlb_world_series_gpt.json")
    ]

    for region, filename in playoff_rounds:
        print(f"Processing {region}...")
        round_data = fetch_and_filter_data(region)
        round_series_structure = create_series_structure(round_data)
        combined_data = merge_original_and_series(round_data, round_series_structure)
        save_to_file(f"/config/www/{filename}", combined_data)
