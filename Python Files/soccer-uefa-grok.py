import urllib.request
import json
from datetime import datetime, timezone

# Define the API URL for UEFA Champions League
API_URLS = {
    #2024 "uefa.champions": "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard?dates=20231218-20240601"
    "uefa.champions": "https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard?dates=20241218-20250601"
}

def fetch_and_filter_data(league):
    try:
        response = urllib.request.urlopen(API_URLS[league])
        data = json.loads(response.read())
        print(f"Raw API response for {league}: {json.dumps(data, indent=2)}")

        # Define playoff slugs for UEFA Champions League
        playoff_slugs = ["round-of-16", "quarterfinals", "semifinals", "final"]

        # Filter events based on status and season slug, including completed matches
        filtered_events = []
        for event in data.get('events', []):
            status = event.get('status', {}).get('type', {}).get('name')
            season_slug = event.get('season', {}).get('slug', '').lower()

            # Include all valid statuses, including completed ones
            if status in ["STATUS_SCHEDULED", "STATUS_IN_PROGRESS", "STATUS_FULL_TIME", "STATUS_FINAL_AET", "STATUS_FINAL_PEN"]:
                if season_slug in playoff_slugs:
                    filtered_events.append(event)

        print(f"Filtered events for {league}: {json.dumps(filtered_events, indent=2)}")
        return {"events": filtered_events}
    except Exception as e:
        print(f"Error fetching data for {league}: {e}")
        return {"events": []}

def determine_round(event, all_events):
    competition = event.get('competitions', [{}])[0]
    event_date = datetime.fromisoformat(event.get('date').replace('Z', '+00:00'))

    sorted_events = sorted(all_events, key=lambda e: datetime.fromisoformat(e.get('date').replace('Z', '+00:00')))
    latest_date = sorted_events[-1]['date'] if sorted_events else event['date']

    # Playoff detection based on season slug
    season_slug = event.get('season', {}).get('slug', '').lower()
    is_playoff_event = season_slug in ["round-of-16", "quarterfinals", "semifinals", "final"]

    # Determine round based on season slug
    if is_playoff_event:
        if season_slug == "round-of-16":
            return "Round of 16"
        elif season_slug == "quarterfinals":
            return "Quarterfinals"
        elif season_slug == "semifinals":
            return "Semifinals"
        elif season_slug == "final" or event['date'] == latest_date:
            return "Final"

    return "Unknown Round"

def create_series_structure(data, league):
    series_dict = {}

    events_with_rounds = []
    for event in data.get('events', []):
        round_name = determine_round(event, data.get('events', []))
        events_with_rounds.append((event, round_name))

    for event, round_name in events_with_rounds:
        for competition in event.get('competitions', []):
            teams = sorted([
                competition['competitors'][0]['team']['displayName'].strip(),
                competition['competitors'][1]['team']['displayName'].strip()
            ])
            series_title = f"{teams[0]} vs {teams[1]} ({round_name})"

            if series_title not in series_dict:
                series_dict[series_title] = {
                    "seriesTitle": series_title,
                    "seriesStatus": "0-0",
                    "seriesDetails": {
                        "Teams": teams,
                        "seriesGames": [],
                        "maxGames": 1 if round_name == "Final" else 2,
                        "stage": round_name
                    }
                }

            status_info = competition.get('status', {})
            game_status = status_info.get('type', {}).get('name', 'scheduled').replace("STATUS_", "").lower()
            time_remaining = status_info.get('displayClock', '0:00') if game_status == "in_progress" else None

            home_team = next((c for c in competition['competitors'] if c['homeAway'] == 'home'), {}).get('team', {})
            away_team = next((c for c in competition['competitors'] if c['homeAway'] == 'away'), {}).get('team', {})
            home_score = next((c['score'] for c in competition['competitors'] if c['homeAway'] == 'home'), '0')
            away_score = next((c['score'] for c in competition['competitors'] if c['homeAway'] == 'away'), '0')

            # Extract logo paths
            home_logo = home_team.get('logo', 'https://via.placeholder.com/16')
            away_logo = away_team.get('logo', 'https://via.placeholder.com/16')

            broadcast = ", ".join(b.get('names', ['TBD'])[0] for b in competition.get('broadcasts', []))

            game_details = {
                "sport": "Soccer",
                "league": league,
                "gameNumber": len(series_dict[series_title]["seriesDetails"]["seriesGames"]) + 1,
                "Date": competition.get('date', 'TBD'),
                "Lowest Seed": {
                    "Name": home_team.get('displayName', 'TBD'),
                    "Score": home_score,
                    "Logo": home_logo
                },
                "Highest Seed": {
                    "Name": away_team.get('displayName', 'TBD'),
                    "Score": away_score,
                    "Logo": away_logo
                },
                "Broadcast": broadcast,
                "Status": game_status,
                "TimeRemaining": time_remaining,
                "Leg": str(competition.get('leg', 1))  # Ensure Leg is a string
            }
            series_dict[series_title]["seriesDetails"]["seriesGames"].append(game_details)

    for series_title, series in series_dict.items():
        team1, team2 = series["seriesDetails"]["Teams"]
        team1_total = 0
        team2_total = 0
        all_games_completed = True

        for game in series["seriesDetails"]["seriesGames"]:
            try:
                if game["Lowest Seed"]["Name"] == team1:
                    team1_total += int(game["Lowest Seed"]["Score"])
                    team2_total += int(game["Highest Seed"]["Score"])
                else:
                    team1_total += int(game["Highest Seed"]["Score"])
                    team2_total += int(game["Lowest Seed"]["Score"])
                if game["Status"] not in ["full_time", "final_aet", "final_pen"]:
                    all_games_completed = False
            except ValueError:
                all_games_completed = False

        round_name = series_title.split("(")[1].rstrip(")")
        if round_name in ["Round of 16", "Quarterfinals", "Semifinals"]:
            if all_games_completed:
                if team1_total > team2_total:
                    series["seriesStatus"] = f"{team1} advances {team1_total}-{team2_total}"
                elif team2_total > team1_total:
                    series["seriesStatus"] = f"{team2} advances {team2_total}-{team1_total}"
                else:
                    series["seriesStatus"] = f"Aggregate tied {team1_total}-{team2_total} (extra time or penalties may decide)"
            else:
                series["seriesStatus"] = f"Aggregate: {team1} {team1_total} - {team2} {team2_total}"
        elif round_name == "Final":
            if all_games_completed and any(game["Status"] in ["full_time", "final_aet", "final_pen"] for game in series["seriesDetails"]["seriesGames"]):
                game = series["seriesDetails"]["seriesGames"][0]
                home_score = int(game["Lowest Seed"]["Score"])
                away_score = int(game["Highest Seed"]["Score"])
                winner = game["Lowest Seed"]["Name"] if home_score > away_score else game["Highest Seed"]["Name"]
                series["seriesStatus"] = f"{winner} wins final {home_score}-{away_score}"
            else:
                series["seriesStatus"] = f"{team1} {team1_total} - {team2} {team2_total}"

    return series_dict

def save_to_file(filename, data):
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")

if __name__ == "__main__":
    print("Fetching UEFA Champions League playoff data...")
    playoff_rounds = [
        ("Round of 16", "soccer_uefa.champions_round_of_16_gpt.json"),
        ("Quarterfinals", "soccer_uefa.champions_quarterfinals_gpt.json"),
        ("Semifinals", "soccer_uefa.champions_semifinals_gpt.json"),
        ("Final", "soccer_uefa.champions_final_gpt.json")
    ]

    for league in API_URLS.keys():
        print(f"Processing {league}...")
        league_data = fetch_and_filter_data(league)
        round_series_structure = create_series_structure(league_data, league)
        
        for round_name, filename in playoff_rounds:
            round_series = [
                s for s in round_series_structure.values()
                if round_name in s["seriesTitle"]
            ]
            round_events = [
                e for e in league_data["events"]
                if any(round_name in s["seriesTitle"] and sorted([
                    e.get('competitions', [{}])[0].get('competitors', [{}])[0].get('team', {}).get('displayName', 'TBD').strip(),
                    e.get('competitions', [{}])[0].get('competitors', [{}])[1].get('team', {}).get('displayName', 'TBD').strip()
                ]) == sorted(s["seriesDetails"]["Teams"]) for s in round_series)
            ]
            print(f"Round {round_name} events for {league}: {json.dumps(round_events, indent=2)}")
            combined_data = {
                "sport": "Soccer",
                "league": league,
                "events": round_events,
                "series": round_series
            }
            save_to_file(f"/config/www/{filename}", combined_data)
