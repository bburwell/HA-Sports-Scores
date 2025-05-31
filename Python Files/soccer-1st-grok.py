import urllib.request
import json
from datetime import datetime, timezone

# Define the API URLs for English Leagues
API_URLS = {
    "eng.2": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.2/scoreboard?dates=20250501-20250610",  # EFL Championship
    "eng.3": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.3/scoreboard?dates=20250501-20250610",  # EFL League One
    "eng.4": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.4/scoreboard?dates=20250501-20250610",  # EFL League Two
    "eng.5": "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.5/scoreboard?dates=20250501-20250610"   # National League
}

def fetch_and_filter_data(league):
    try:
        response = urllib.request.urlopen(API_URLS[league])
        data = json.loads(response.read())
        print(f"Raw API response for {league}: {json.dumps(data, indent=2)}")

        # Define playoff slugs for eng.4 and eng.5
        playoff_slugs = ["elimination-round", "promotion-semifinals", "promotion-final"]

        # Filter events based on status and, for eng.4/eng.5, season slug
        filtered_events = []
        for event in data.get('events', []):
            status = event.get('status', {}).get('type', {}).get('name')
            season_slug = event.get('season', {}).get('slug', '').lower()

            # Base filter: only keep events with valid statuses
            if status not in ["STATUS_SCHEDULED", "STATUS_IN_PROGRESS", "STATUS_FULL_TIME", "STATUS_FINAL_AET", "STATUS_FINAL_PEN"]:
                continue

            # Additional filter for eng.4 and eng.5: only keep playoff events
            if league in ["eng.4", "eng.5"]:
                if season_slug in playoff_slugs:
                    filtered_events.append(event)
            else:
                # For eng.2 and eng.3, keep all events with valid status
                filtered_events.append(event)

        print(f"Filtered events for {league}: {json.dumps(filtered_events, indent=2)}")
        return {"events": filtered_events}
    except Exception as e:
        print(f"Error fetching data for {league}: {e}")
        return {"events": []}

def determine_round(event, all_events):
    competition = event.get('competitions', [{}])[0]
    leg = competition.get('leg', {}).get('value', 1)
    event_date = datetime.fromisoformat(event.get('date').replace('Z', '+00:00'))

    sorted_events = sorted(all_events, key=lambda e: datetime.fromisoformat(e.get('date').replace('Z', '+00:00')))
    latest_date = sorted_events[-1]['date'] if sorted_events else event['date']

    teams = sorted([
        competition.get('competitors', [{}])[0].get('team', {}).get('displayName', 'TBD').strip(),
        competition.get('competitors', [{}])[1].get('team', {}).get('displayName', 'TBD').strip()
    ])
    matching_events = [
        e for e in all_events
        if sorted([
            e.get('competitions', [{}])[0].get('competitors', [{}])[0].get('team', {}).get('displayName', 'TBD').strip(),
            e.get('competitions', [{}])[0].get('competitors', [{}])[1].get('team', {}).get('displayName', 'TBD').strip()
        ]) == teams
    ]

    # Playoff detection based on season slug
    event_name = event.get('name', '').lower()
    season = event.get('season', {})
    season_slug = season.get('slug', '').lower()
    season_type = season.get('type', 0)
    notes = [note.get('text', '').lower() for note in competition.get('notes', [])]
    is_playoff_event = (
        'playoff' in event_name or 'semifinal' in event_name or 'promotion' in event_name or
        'final' in event_name or 'relegation' in event_name or
        'promotion-semifinals' in season_slug or 'promotion-final' in season_slug or
        'elimination-round' in season_slug or
        any('leg' in note for note in notes) or any('aggregate' in note for note in notes) or
        any('eliminator' in note for note in notes) or any('final' in note for note in notes) or
        any('promotion' in note for note in notes) or any('relegation' in note for note in notes) 
    )

    # Determine round based on league and season slug
    league = event.get('league', {}).get('abbreviation', 'eng.3')
    is_eliminator = False
    is_semifinal = False
    is_final = False

    if is_playoff_event:
        if league == "eng.5":  # National League (6-team playoffs)
            if 'elimination-round' in season_slug:
                is_eliminator = True
            elif 'promotion-semifinals' in season_slug:
                is_semifinal = True
            elif 'promotion-final' in season_slug or event['date'] == latest_date:
                is_final = True
        elif league == "eng.4":  # EFL League Two (4-team playoffs)
            if 'promotion-semifinals' in season_slug:
                is_semifinal = True
            elif 'promotion-final' in season_slug or event['date'] == latest_date:
                is_final = True
        else:  # EFL Championship and League One (eng.2, eng.3) - 4-team, two-leg playoffs
            is_semifinal = is_playoff_event and any('leg' in note for note in notes) and not (event['date'] == latest_date)
            is_final = is_playoff_event and event['date'] == latest_date and len(matching_events) == 1

    print(f"Event ID: {event.get('id')}, Teams: {teams}, Leg: {leg}, Matching Events: {len(matching_events)}, Event Name: {event_name}, Season Slug: {season_slug}, Season Type: {season_type}, Notes: {notes}, Is Playoff: {is_playoff_event}, Is Eliminator: {is_eliminator}, Is Semifinal: {is_semifinal}, Is Final: {is_final}, Date: {event['date']}, Latest Date: {latest_date}")

    if is_eliminator and league == "eng.5":
        print(f"Classified as Eliminator: {event.get('id')}")
        return "Eliminator"
    elif is_semifinal:
        print(f"Classified as Semifinals: {event.get('id')}")
        return "Semifinals"
    elif is_final:
        print(f"Classified as Final: {event.get('id')}")
        return "Final"
    print(f"Classified as Unknown Round: {event.get('id')}")
    return "Unknown Round"

def create_series_structure(data, league):
    series_dict = {}
    team_abbr_to_name = {}

    events_with_rounds = []
    for event in data.get('events', []):
        round_name = determine_round(event, data.get('events', []))
        events_with_rounds.append((event, round_name))

    for event, round_name in events_with_rounds:
        for competition in event.get('competitions', []):
            team1 = competition['competitors'][0]['team']
            team2 = competition['competitors'][1]['team']

            team_abbr_to_name[team1['abbreviation']] = team1['displayName']
            team_abbr_to_name[team2['abbreviation']] = team2['displayName']

            teams = sorted([team1['displayName'].strip(), team2['displayName'].strip()])
            series_title = f"{teams[0]} vs {teams[1]} ({round_name})"

            if series_title not in series_dict:
                series_dict[series_title] = {
                    "seriesTitle": series_title,
                    "seriesStatus": "0-0",
                    "seriesDetails": {
                        "Teams": teams,
                        "seriesGames": [],
                        "maxGames": 2 if round_name in ["Semifinals"] and league != "eng.5" else 1
                    }
                }

            status_info = competition.get('status', {})
            game_status = status_info.get('type', {}).get('name', 'scheduled').replace("STATUS_", "").lower()
            game_segment = None
            time_remaining = status_info.get('displayClock', '0:00') if game_status == "in_progress" else None

            home_team = next((c for c in competition['competitors'] if c['homeAway'] == 'home'), {}).get('team', {})
            away_team = next((c for c in competition['competitors'] if c['homeAway'] == 'away'), {}).get('team', {})
            home_score = next((c['score'] for c in competition['competitors'] if c['homeAway'] == 'home'), '0')
            away_score = next((c['score'] for c in competition['competitors'] if c['homeAway'] == 'away'), '0')

            broadcast = ", ".join(
                b.get('names', ['TBD'])[0] for b in competition.get('broadcasts', [])
            )

            game_details = {
                "sport": "Soccer",
                "league": league,
                "gameNumber": len(series_dict[series_title]["seriesDetails"]["seriesGames"]) + 1,
                "Date": competition.get('date', 'TBD'),
                "HomeTeam": {
                    "Name": home_team.get('displayName', 'TBD'),
                    "Score": home_score,
                    "Logo": home_team.get('logo', '')
                },
                "AwayTeam": {
                    "Name": away_team.get('displayName', 'TBD'),
                    "Score": away_score,
                    "Logo": away_team.get('logo', '')
                },
                "Broadcast": broadcast,
                "Status": game_status,
                "GameSegment": game_segment,
                "TimeRemaining": time_remaining,
                "Leg": competition.get('leg', '1')
            }
            series_dict[series_title]["seriesDetails"]["seriesGames"].append(game_details)

    for series_title, series in series_dict.items():
        team1, team2 = series["seriesDetails"]["Teams"]
        team1_total = 0
        team2_total = 0

        for game in series["seriesDetails"]["seriesGames"]:
            try:
                if game["HomeTeam"]["Name"] == team1:
                    team1_total += int(game["HomeTeam"]["Score"])
                    team2_total += int(game["AwayTeam"]["Score"])
                else:
                    team1_total += int(game["AwayTeam"]["Score"])
                    team2_total += int(game["HomeTeam"]["Score"])
            except ValueError:
                continue

        round_name = series_title.split("(")[1].rstrip(")")
        if round_name == "Semifinals":
            if all(game["Status"] == "full_time" for game in series["seriesDetails"]["seriesGames"]):
                if team1_total > team2_total:
                    series["seriesStatus"] = f"{team1} advances {team1_total}-{team2_total}"
                elif team2_total > team1_total:
                    series["seriesStatus"] = f"{team2} advances {team2_total}-{team1_total}"
                else:
                    series["seriesStatus"] = f"Aggregate tied {team1_total}-{team2_total} (extra time or penalties may decide)"
            else:
                series["seriesStatus"] = f"Aggregate: {team1} {team1_total} - {team2} {team2_total}"
        elif round_name == "Final":
            if any(game["Status"] in ["full_time", "final_aet", "final_pen"] for game in series["seriesDetails"]["seriesGames"]):
                game = series["seriesDetails"]["seriesGames"][0]
                home_score = int(game["HomeTeam"]["Score"])
                away_score = int(game["AwayTeam"]["Score"])
                winner = game["HomeTeam"]["Name"] if home_score > away_score else game["AwayTeam"]["Name"]
                series["seriesStatus"] = f"{winner} wins final"
            else:
                series["seriesStatus"] = f"{team1} vs {team2}"
        elif round_name == "Eliminator":
            if any(game["Status"] in ["full_time", "final_aet", "final_pen"] for game in series["seriesDetails"]["seriesGames"]):
                game = series["seriesDetails"]["seriesGames"][0]
                home_score = int(game["HomeTeam"]["Score"])
                away_score = int(game["AwayTeam"]["Score"])
                winner = game["HomeTeam"]["Name"] if home_score > away_score else game["AwayTeam"]["Name"]
                series["seriesStatus"] = f"{winner} advances"
            else:
                series["seriesStatus"] = f"{team1} vs {team2}"

    return series_dict

def merge_original_and_series(data, series):
    return {
        "sport": "Soccer",
        "league": list(data.keys())[0] if data else "eng.3",
        "events": data.get(list(data.keys())[0], {}).get("events", []),
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
    print("Fetching soccer promotion playoff data...")
    playoff_rounds = [
        ("Eliminator", "soccer_{}_eliminator_gpt.json"),
        ("Semifinals", "soccer_{}_semifinals_gpt.json"),
        ("Final", "soccer_{}_final_gpt.json")
    ]

    for league in API_URLS.keys():
        print(f"Processing {league}...")
        league_data = fetch_and_filter_data(league)
        round_data = {league: league_data}
        round_series_structure = create_series_structure(round_data[league], league)
        
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
            save_to_file(f"/config/www/{filename.format(league)}", combined_data)
