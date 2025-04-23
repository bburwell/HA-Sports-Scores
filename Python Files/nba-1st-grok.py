import urllib.request
import json
from datetime import datetime, timezone

# Define the API URL for fetching NBA playoff data
API_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20250415-20250622"

def fetch_and_filter_data(region):
    try:
        # Fetch data using urllib
        response = urllib.request.urlopen(API_URL)
        data = json.loads(response.read())

        # Filter the events based on the notes field for the specified region
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

def create_series_structure(data):
    # Dictionary to group games by series title
    series_dict = {}

    for event in data.get('events', []):
        for competition in event.get('competitions', []):  # Iterate over each competition/game
            team1 = competition['competitors'][0]['team']
            team2 = competition['competitors'][1]['team']

            # Extract seed numbers (if available) to determine lowest/highest seed
            seed1 = competition['competitors'][0].get('seed', float('inf'))
            seed2 = competition['competitors'][1].get('seed', float('inf'))

            if seed1 < seed2:
                lowest_seed, highest_seed = team1, team2
            else:
                lowest_seed, highest_seed = team2, team1

            # Ensure consistent series title
            series_title = " vs ".join(sorted([lowest_seed['displayName'], highest_seed['displayName']]))

            # Initialize series entry if it doesn't exist
            if series_title not in series_dict:
                series_dict[series_title] = {
                    "seriesTitle": series_title,
                    "seriesStatus": "0-0",
                    "seriesDetails": {
                        "Teams": [lowest_seed['displayName'], highest_seed['displayName']],
                        "seriesGames": []
                    }
                }

            # Determine game status and live details
            status_info = competition.get('status', {})
            game_status = "scheduled"
            game_segment = None
            time_remaining = None

            # Check the game status from the API
            if status_info.get('type', {}).get('completed', False):
                game_status = "final"
            elif status_info.get('type', {}).get('state') == "in":  # Game is in progress
                game_status = "live"
                period_num = status_info.get('period', 0)
                # NBA periods: 1st, 2nd, 3rd, 4th, OT (overtime)
                if period_num <= 4:
                    game_segment = f"{period_num}{'st' if period_num == 1 else 'nd' if period_num == 2 else 'rd' if period_num == 3 else 'th'}"
                else:
                    game_segment = "OT"  # Overtime in NBA playoffs
                time_remaining = status_info.get('displayClock', '0:00')
            else:
                game_status = "scheduled"

            # Add game details under the series
            game_details = {
                "sport": "NBA",  # Add sport identifier at the game level for template access
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
                "GameSegment": game_segment,  # Standardized field name
                "TimeRemaining": time_remaining
            }
            series_dict[series_title]["seriesDetails"]["seriesGames"].append(game_details)

    # Calculate series status
    for series in series_dict.values():
        team1 = series["seriesDetails"]["Teams"][0]
        team2 = series["seriesDetails"]["Teams"][1]
        team1_wins = 0
        team2_wins = 0

        for game in series["seriesDetails"]["seriesGames"]:
            # Ensure scores are numeric and not "TBD"
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

        # Update seriesStatus based on wins
        if team1_wins > team2_wins:
            series["seriesStatus"] = f"{team1} leads series {team1_wins}-{team2_wins}"
        elif team2_wins > team1_wins:
            series["seriesStatus"] = f"{team2} leads series {team2_wins}-{team1_wins}"  # Fixed bug
        else:
            series["seriesStatus"] = f"Series tied {team1_wins}-{team2_wins}"

    return series_dict

def merge_original_and_series(data, series):
    # Merge original events with structured series data
    return {
        "sport": "NBA",  # Add sport identifier at root level for consistency
        "events": data.get("events", []),  # Keep original event data
        "series": list(series.values())  # Store series under deeper structure
    }

def save_to_file(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

# Main execution
if __name__ == "__main__":
    print("Fetching NBA playoff data...")

    # Define all playoff rounds and their corresponding regions
    playoff_rounds = [
        ("East 1st Round", "nba_east_1st_round_gpt.json"),
        ("West 1st Round", "nba_west_1st_round_gpt.json"),
        ("East 2nd Round", "nba_east_2nd_round_gpt.json"),
        ("West 2nd Round", "nba_west_2nd_round_gpt.json"),
        ("East Final", "nba_east_final_gpt.json"),
        ("West Final", "nba_west_final_gpt.json"),
        ("NBA Finals", "nba_finals_gpt.json")
    ]

    # Process each playoff round
    for region, filename in playoff_rounds:
        print(f"Processing {region}...")
        # Fetch and filter data for the round
        round_data = fetch_and_filter_data(region)
        # Create structured series-based data
        round_series_structure = create_series_structure(round_data)
        # Merge original events and formatted series structure
        combined_data = merge_original_and_series(round_data, round_series_structure)
        # Save structured data
        save_to_file(f"/config/www/{filename}", combined_data)
