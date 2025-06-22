import urllib.request
import json
from datetime import datetime, timezone

# Define the API URL for fetching 2025 Concacaf Gold Cup live data
API_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.gold/scoreboard?dates=20250614-20250706"

# Group assignments based on 2025 Concacaf Gold Cup draw
GROUP_TEAMS = {
    "A": ["Mexico", "Costa Rica", "Suriname", "Dominican Republic"],
    "B": ["Canada", "Honduras", "El Salvador", "Curacao"],
    "C": ["Panama", "Jamaica", "Guatemala", "Guadeloupe"],
    "D": ["United States", "Haiti", "Trinidad and Tobago", "Saudi Arabia"]
}

def fetch_and_filter_data(stage_or_group):
    try:
        response = urllib.request.urlopen(API_URL)
        data = json.loads(response.read())
        print("Full API response length:", len(data.get('events', [])))  # Debug: Total events
        if stage_or_group.startswith("group-"):
            group_letter = stage_or_group.split("-")[1].upper()
            group_teams = [t.lower() for t in GROUP_TEAMS[group_letter]]
            filtered_events = [
                event for event in data.get('events', [])
                if event.get('season', {}).get('slug') == "group-stage"
                and any(t.lower() in (event.get('name', '').lower() or ''.join(c['team']['displayName'].lower() for c in event.get('competitions', [{}])[0].get('competitors', []))) for t in group_teams)
            ]
            print(f"Filtered events for {stage_or_group}: {len(filtered_events)}")
            return {"events": filtered_events}
        else:
            filtered_events = [
                event for event in data.get('events', [])
                if event.get('season', {}).get('slug') == stage_or_group
            ]
            print(f"Filtered events for {stage_or_group}: {len(filtered_events)}")
            return {"events": filtered_events}
    except Exception as e:
        print(f"Error fetching data for {stage_or_group}: {e}")
        return {"events": []}

def extract_round_name(stage_or_group):
    round_map = {
        "group-A": "Group A", "group-B": "Group B", "group-C": "Group C", "group-D": "Group D",
        "quarterfinals": "Quarter-finals",
        "semifinals": "Semifinals", "final": "Final"
    }
    return round_map.get(stage_or_group, "Unknown Round")

def create_series_structure(data, stage_or_group):
    if not data['events']:
        return {}

    first_event = data['events'][0]
    slug = first_event.get('season', {}).get('slug', 'unknown')
    stage = extract_round_name(stage_or_group)

    # Extract all teams and matches, limited to the defined group
    group_letter = stage_or_group.split("-")[1].upper() if stage_or_group.startswith("group-") else None
    all_teams = set(GROUP_TEAMS.get(group_letter, [])) if group_letter else set()
    all_games = []
    print(f"Processing events for {stage_or_group}: {len(data['events'])} events")  # Debug
    
    # Map team names to logos
    team_logo_map = {}
    for event in data['events']:
        for competition in event.get('competitions', []):
            for competitor in competition.get('competitors', []):
                team_name = competitor['team']['displayName']
                team_logo = competitor['team'].get('logo', '')
                team_logo_map[team_name] = team_logo

    for event in data['events']:
        for competition in event.get('competitions', []):
            team1 = competition['competitors'][0]['team']['displayName']
            team2 = competition['competitors'][1]['team']['displayName']
            if group_letter and (team1 not in GROUP_TEAMS[group_letter] or team2 not in GROUP_TEAMS[group_letter]):
                continue  # Skip games not involving group teams
            print(f"Matched game: {team1} vs {team2}")  # Debug
            all_teams.add(team1)
            all_teams.add(team2)

            status = competition.get('status', {}).get('type', {})
            game_status = status.get('state', 'scheduled')
            if status.get('completed', False):
                game_status = "full_time"
            elif status.get('state') == "in":
                game_status = "live"

            broadcast = ", ".join(b.get('names', ['TBD'])[0] for b in competition.get('broadcasts', []) if b.get('names'))
            venue = competition.get('venue', {}).get('fullName', 'TBD')
            date = competition.get('date', 'TBD')

            # Determine seeds based on alphabetical order
            if team1 <= team2:
                lowest_team, highest_team = team1, team2
                lowest_score = str(competition['competitors'][0].get('score', 0))
                highest_score = str(competition['competitors'][1].get('score', 0))
                lowest_advance = competition['competitors'][0].get('advance', False)
                highest_advance = competition['competitors'][1].get('advance', False)
            else:
                lowest_team, highest_team = team2, team1
                lowest_score = str(competition['competitors'][1].get('score', 0))
                highest_score = str(competition['competitors'][0].get('score', 0))
                lowest_advance = competition['competitors'][1].get('advance', False)
                highest_advance = competition['competitors'][0].get('advance', False)

            game = {
                "gameNumber": len(all_games) + 1,
                "Date": date,
                "Lowest Seed": {
                    "Name": lowest_team,
                    "Score": lowest_score,
                    "Logo": team_logo_map.get(lowest_team, ''),
                    "Advance": lowest_advance
                },
                "Highest Seed": {
                    "Name": highest_team,
                    "Score": highest_score,
                    "Logo": team_logo_map.get(highest_team, ''),
                    "Advance": highest_advance
                },
                "Broadcast": broadcast,
                "Status": game_status,
                "Venue": venue
            }
            all_games.append(game)

    # Calculate advancing teams
    advancing_teams = set()
    if stage.startswith("Group"):
        team_points = {team: 0 for team in all_teams}
        team_goals_for = {team: 0 for team in all_teams}
        team_goals_against = {team: 0 for team in all_teams}
        team_played = {team: 0 for team in all_teams}

        for game in all_games:
            if game["Status"] == "full_time":
                team1 = game["Lowest Seed"]["Name"]
                team2 = game["Highest Seed"]["Name"]
                team1_score = int(game["Lowest Seed"]["Score"])
                team2_score = int(game["Highest Seed"]["Score"])

                team_played[team1] += 1
                team_played[team2] += 1
                team_goals_for[team1] += team1_score
                team_goals_for[team2] += team2_score
                team_goals_against[team1] += team2_score
                team_goals_against[team2] += team1_score

                if team1_score > team2_score:
                    team_points[team1] += 3
                elif team2_score > team1_score:
                    team_points[team2] += 3
                else:
                    team_points[team1] += 1
                    team_points[team2] += 1

        # Sort teams by points, goal difference, then goals for
        sorted_teams = sorted(all_teams, key=lambda x: (
            team_points[x],
            team_goals_for[x] - team_goals_against[x],
            team_goals_for[x]
        ), reverse=True)
        advancing_teams = set(sorted_teams[:2])  # Top 2 teams advance
    elif stage in ["Round of 16", "Quarter-finals", "Semifinals", "Final"]:
        for game in all_games:
            if game["Status"] in ["full_time", "live"]:
                team1_score = int(game["Lowest Seed"]["Score"])
                team2_score = int(game["Highest Seed"]["Score"])
                team1 = game["Lowest Seed"]["Name"]
                team2 = game["Highest Seed"]["Name"]

                if team1_score > team2_score:
                    advancing_teams.add(team1)
                elif team2_score > team1_score:
                    advancing_teams.add(team2)
                elif game["Lowest Seed"]["Advance"]:
                    advancing_teams.add(team1)
                elif game["Highest Seed"]["Advance"]:
                    advancing_teams.add(team2)

    series_title = f"{stage} Matches"
    series_status = f"{stage} {('Standings' if stage.startswith('Group') else 'Matches')}"
    if stage == "Round of 16" and len(advancing_teams) > 16:
        advancing_teams = set(list(advancing_teams)[:16])  # Limit to 16 for Round of 16

    return {
        series_title: {
            "seriesTitle": series_title,
            "seriesStatus": series_status,
            "seriesDetails": {
                "stage": stage,
                "Teams": list(all_teams),
                "AdvancingTeams": list(advancing_teams),
                "seriesGames": all_games,
                "maxGames": 6 if stage.startswith("Group") else (len(all_games) if all_games else 0),  # 6 group games max
                "sport": "Soccer",
                "slug": stage_or_group
            }
        }
    }

def merge_original_and_series(data, series):
    return {
        "sport": "Soccer",
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
    print("Fetching 2025 Concacaf Gold Cup live data...")
    concacaf_gold_cup_stages = [
        ("group-A", "/config/www/concacaf_gold_cup_group_a_gpt.json"),
        ("group-B", "/config/www/concacaf_gold_cup_group_b_gpt.json"),
        ("group-C", "/config/www/concacaf_gold_cup_group_c_gpt.json"),
        ("group-D", "/config/www/concacaf_gold_cup_group_d_gpt.json"),
        ("round-of-16", "/config/www/concacaf_gold_cup_round_of_16_gpt.json"),
        ("quarterfinals", "/config/www/concacaf_gold_cup_quarterfinals_gpt.json"),
        ("semifinals", "/config/www/concacaf_gold_cup_semifinals_gpt.json"),
        ("final", "/config/www/concacaf_gold_cup_final_gpt.json")
    ]

    for stage_or_group, filename in concacaf_gold_cup_stages:
        print(f"Processing {stage_or_group}...")
        round_data = fetch_and_filter_data(stage_or_group)
        round_series_structure = create_series_structure(round_data, stage_or_group)
        combined_data = merge_original_and_series(round_data, round_series_structure)
        save_to_file(filename, combined_data)
