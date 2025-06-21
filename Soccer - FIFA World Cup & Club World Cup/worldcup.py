import urllib.request
import json
from datetime import datetime, timezone

# Define the API URL for fetching World Cup 2022 data
API_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20221120-20221218"

# Manual group assignments based on 2022 World Cup schedule (simplified)
GROUP_TEAMS = {
    "A": ["Qatar", "Ecuador", "Senegal", "Netherlands"],
    "B": ["England", "Iran", "United States", "Wales"],
    "C": ["Argentina", "Saudi Arabia", "Mexico", "Poland"],
    "D": ["France", "Australia", "Denmark", "Tunisia"],
    "E": ["Spain", "Costa Rica", "Germany", "Japan"],
    "F": ["Belgium", "Canada", "Morocco", "Croatia"],
    "G": ["Brazil", "Serbia", "Switzerland", "Cameroon"],
    "H": ["Portugal", "Ghana", "Uruguay", "Korea Republic"]
}

def fetch_and_filter_data(slug_or_group):
    try:
        response = urllib.request.urlopen(API_URL)
        data = json.loads(response.read())
        print("Full API response length:", len(data.get('events', [])))  # Debug: Total events
        if slug_or_group.startswith("group-stage:"):
            group_letter = slug_or_group.split(":")[1].upper()
            group_teams = [t.lower() for t in GROUP_TEAMS[group_letter]]
            filtered_events = [
                event for event in data.get('events', [])
                if event.get('season', {}).get('slug') == "group-stage"
                and any(t.lower() in event['name'].lower() for t in group_teams)
            ]
            print(f"Filtered events for {slug_or_group}: {len(filtered_events)}")
            return {"events": filtered_events}
        else:
            filtered_events = [
                event for event in data.get('events', [])
                if event.get('season', {}).get('slug') == slug_or_group
            ]
            print(f"Filtered events for {slug_or_group}: {len(filtered_events)}")
            return {"events": filtered_events}
    except Exception as e:
        print(f"Error fetching data for {slug_or_group}: {e}")
        return {"events": []}

def extract_round_name(slug_or_group):
    round_map = {
        "group-stage:A": "Group A",
        "group-stage:B": "Group B",
        "group-stage:C": "Group C",
        "group-stage:D": "Group D",
        "group-stage:E": "Group E",
        "group-stage:F": "Group F",
        "group-stage:G": "Group G",
        "group-stage:H": "Group H",
        "round-of-16": "Round of 16",
        "quarterfinals": "Quarter-finals",
        "semifinals": "Semifinals",
        "3rd-place": "3rd Place",
        "final": "Final"
    }
    return round_map.get(slug_or_group, "Unknown Round")

def create_series_structure(data, slug_or_group):
    if not data['events']:
        return {}

    first_event = data['events'][0]
    slug = first_event.get('season', {}).get('slug', 'unknown')
    stage = extract_round_name(slug_or_group)

    # Extract all teams and matches
    all_teams = set()
    all_games = []
    for event in data['events']:
        for competition in event.get('competitions', []):
            team1 = competition['competitors'][0]['team']['displayName']
            team2 = competition['competitors'][1]['team']['displayName']
            all_teams.add(team1)
            all_teams.add(team2)

            status = competition.get('status', {}).get('type', {})
            game_status = "scheduled"
            if status.get('completed', False):
                game_status = "full_time"
            elif status.get('state') == "in":
                game_status = "live"

            broadcast = ", ".join(b.get('names', ['TBD'])[0] for b in competition.get('broadcasts', []) if b.get('names'))
            venue = competition.get('venue', {}).get('fullName', 'TBD')
            date = competition.get('date', 'TBD')

            game = {
                "gameNumber": len(all_games) + 1,
                "Date": date,
                "Lowest Seed": {
                    "Name": min(team1, team2),  # Simple sorting for consistency
                    "Score": competition['competitors'][0].get('score', '0'),
                    "Logo": competition['competitors'][0]['team'].get('logo', ''),
                    "Advance": competition['competitors'][0].get('advance', False)
                },
                "Highest Seed": {
                    "Name": max(team1, team2),
                    "Score": competition['competitors'][1].get('score', '0'),
                    "Logo": competition['competitors'][1]['team'].get('logo', ''),
                    "Advance": competition['competitors'][1].get('advance', False)
                },
                "Broadcast": broadcast,
                "Status": game_status,
                "Venue": venue
            }
            all_games.append(game)

    # Calculate standings for group stages
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
    elif stage in ["Round of 16", "Quarter-finals", "Semifinals", "3rd Place", "Final"]:
        for game in all_games:
            if game["Status"] == "full_time":
                team1_score = int(game["Lowest Seed"]["Score"])
                team2_score = int(game["Highest Seed"]["Score"])
                team1 = game["Lowest Seed"]["Name"]
                team2 = game["Highest Seed"]["Name"]

                # Determine winner based on score if Advance is not set or unreliable
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
    if stage == "Round of 16" and len(advancing_teams) > 8:
        advancing_teams = set(list(advancing_teams)[:8])  # Limit to 8 for Round of 16

    return {
        series_title: {
            "seriesTitle": series_title,
            "seriesStatus": series_status,
            "seriesDetails": {
                "stage": stage,
                "Teams": list(all_teams),
                "AdvancingTeams": list(advancing_teams),
                "seriesGames": all_games,
                "maxGames": len(all_games) if all_games else 0,
                "sport": "Soccer",
                "slug": slug_or_group
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
    print("Fetching World Cup 2022 data...")
    worldcup_rounds = [
        ("group-stage:A", "worldcup_group_a_gpt.json"),
        ("group-stage:B", "worldcup_group_b_gpt.json"),
        ("group-stage:C", "worldcup_group_c_gpt.json"),
        ("group-stage:D", "worldcup_group_d_gpt.json"),
        ("group-stage:E", "worldcup_group_e_gpt.json"),
        ("group-stage:F", "worldcup_group_f_gpt.json"),
        ("group-stage:G", "worldcup_group_g_gpt.json"),
        ("group-stage:H", "worldcup_group_h_gpt.json"),
        ("round-of-16", "worldcup_round_of_16_gpt.json"),
        ("quarterfinals", "worldcup_quarterfinals_gpt.json"),
        ("semifinals", "worldcup_semifinals_gpt.json"),
        ("3rd-place", "worldcup_3rd_place_gpt.json"),
        ("final", "worldcup_final_gpt.json")
    ]

    for slug_or_group, filename in worldcup_rounds:
        print(f"Processing {slug_or_group}...")
        round_data = fetch_and_filter_data(slug_or_group)
        round_series_structure = create_series_structure(round_data, slug_or_group)
        combined_data = merge_original_and_series(round_data, round_series_structure)
        save_to_file(filename, combined_data)
